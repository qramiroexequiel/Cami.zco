# Documentación Técnica y Comercial - Proyecto cami.zco

**Versión**: 1.0  
**Fecha**: 2025  
**Tipo de Proyecto**: Sistema Web de Catálogo y Gestión de Pedidos Personalizados

---

## 1. ¿Qué hace este proyecto?

### Problema que resuelve

El proyecto **cami.zco** es una plataforma web desarrollada para negocios de productos personalizados (específicamente vasos, copas y artículos con grabado láser o personalización artesanal) que necesitan:

1. **Mostrar un catálogo de productos** de forma profesional y atractiva
2. **Gestionar pedidos personalizados** sin necesidad de pasarelas de pago complejas
3. **Comunicarse con clientes** mediante WhatsApp como canal principal de contacto y confirmación
4. **Administrar el negocio** a través de un panel de gestión intuitivo
5. **Optimizar conversiones** facilitando el proceso desde la visualización del producto hasta la confirmación del pedido

### Tipo de producto

Este proyecto es un **Sistema de Catálogo Web con Gestión de Pedidos Asistida**, también conocido como "E-commerce asistido" o "Catálogo con pedidos por WhatsApp". No es un e-commerce tradicional con carrito y checkout automático, sino una plataforma que:

- Presenta productos de forma visual y organizada
- Permite a los clientes completar un formulario de pedido detallado
- Genera un mensaje prearmado para WhatsApp con toda la información
- Facilita la gestión posterior del pedido mediante un panel administrativo

### Valor que aporta al negocio

1. **Presencia web profesional**: Sitio web moderno, responsive y optimizado para móviles que genera confianza en potenciales clientes
2. **Automatización del proceso inicial**: Reduce el tiempo que el negocio dedica a recibir consultas repetitivas, ya que el cliente completa un formulario estructurado con toda la información necesaria
3. **Mejora de conversión**: El proceso guiado y la integración directa con WhatsApp eliminan fricciones y aumentan la probabilidad de que una consulta se convierta en pedido
4. **Gestión centralizada**: Todos los pedidos y consultas quedan registrados en un sistema, facilitando el seguimiento y la organización
5. **Escalabilidad**: Permite gestionar múltiples productos, categorías y pedidos sin aumentar proporcionalmente el esfuerzo operativo
6. **Métrica y seguimiento**: Integración opcional con Google Analytics 4 para medir el rendimiento del sitio

---

## 2. ¿Para quién está hecho?

### Tipo de cliente/negocio final

El sistema está diseñado para **emprendimientos y pequeñas empresas** que:

- Ofrecen productos personalizados o hechos a medida (grabado en vidrio, cerámica, madera, metales, etc.)
- Utilizan WhatsApp como canal principal de comunicación con clientes
- Necesitan mostrar un catálogo visual pero no requieren pagos online automáticos
- Prefieren un proceso de pedido guiado que luego se confirma personalmente por WhatsApp
- Buscan una solución económica y fácil de mantener

**Ejemplos de negocios ideales:**
- Talleres de grabado láser
- Artesanos que personalizan objetos
- Tiendas de regalos personalizados
- Servicios de impresión y personalización
- Negocios que venden productos "por encargo" o bajo pedido

### Tipo de usuario

El sistema tiene dos tipos principales de usuarios:

#### A. Cliente final (usuario público, sin autenticación)

**Perfil:**
- Personas que buscan productos personalizados como regalos o artículos únicos
- Usuarios que navegan desde dispositivos móviles principalmente
- Clientes que prefieren comunicarse por WhatsApp antes de realizar una compra

**Flujo de uso:**
1. **Navegación del catálogo**: Explora la página de inicio con productos destacados
2. **Búsqueda por categorías**: Accede al catálogo completo y filtra por categorías
3. **Visualización de producto**: Revisa detalles, imágenes, precio y tiempo estimado
4. **Inicio de pedido**: Hace clic en "Hacé tu pedido" (desde el producto o desde el menú)
5. **Completar formulario**: Ingresa datos personales, selecciona producto (si no venía desde uno específico), cantidad, texto a grabar, fecha necesaria, método de entrega
6. **Confirmación**: Recibe una página de confirmación con un botón/link directo a WhatsApp con el mensaje prearmado
7. **Comunicación externa**: Se comunica con el negocio por WhatsApp para finalizar el pedido (confirmación de precio, detalles, pago, etc.)

**Páginas disponibles:**
- Home (`/`): Landing page con hero, productos destacados, galería, proceso, FAQ
- Catálogo (`/catalogo/`): Lista completa de productos con filtros
- Detalle de producto (`/catalogo/<slug>/`): Vista detallada de un producto
- Formulario de pedido (`/pedir/` o `/pedir/<producto-slug>/`): Formulario de pedido
- Confirmación de pedido (`/confirmacion/<pedido-id>/`): Página de confirmación con link a WhatsApp
- Formulario de consultas (`/contacto/`): Para consultas generales (no pedidos)

#### B. Administrador/Operador del negocio (usuario autenticado)

**Perfil:**
- Propietario del negocio o persona encargada de gestionar pedidos
- Usuario con conocimientos básicos de computación
- Necesita acceso desde cualquier dispositivo para revisar pedidos

**Flujo de uso:**
1. **Acceso al dashboard**: Inicia sesión en `/dashboard/` o `/admin/`
2. **Revisión de pedidos nuevos**: Ve pedidos pendientes en la página principal del dashboard
3. **Gestión de pedidos**: Actualiza estados de pedidos (Nuevo → Confirmado → En producción → Listo → Entregado), agrega notas internas
4. **Gestión de productos**: Crea, edita, activa/desactiva productos desde el dashboard simplificado
5. **Configuración**: Modifica número de WhatsApp, Instagram, textos del sitio desde el panel
6. **Administración avanzada**: Accede al admin de Django para gestionar categorías, imágenes, secciones de la home, FAQ, galería

**Paneles disponibles:**
- **Dashboard personalizado** (`/dashboard/`): Panel simplificado con estadísticas, gestión rápida de productos y pedidos
- **Admin de Django** (`/admin/`): Panel completo para gestión avanzada de todo el contenido

---

## 3. Arquitectura general

### Framework principal

El proyecto está construido sobre **Django 6.0**, un framework web de alto nivel escrito en Python, reconocido por su robustez, seguridad y escalabilidad en aplicaciones de producción.

### Patrón de arquitectura utilizado

El proyecto sigue el **patrón MVT (Model-View-Template)** estándar de Django, con una organización modular por aplicaciones:

```
┌─────────────────────────────────────────────┐
│         CAMI_ZCO (Proyecto Principal)       │
│  - settings.py (Configuración central)      │
│  - urls.py (Enrutamiento principal)         │
│  - wsgi.py (Entry point producción)         │
│  - context_processors.py (Contextos globales)│
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
    ┌───▼───┐  ┌───▼───┐  ┌───▼───┐
    │CATALOG│  │PEDIDOS│  │CONTACTO│
    │   O   │  │       │  │        │
    └───────┘  └───────┘  └────────┘
        │           │
    ┌───▼───────────▼───┐
    │    DASHBOARD      │
    │ (Gestión unificada)│
    └───────────────────┘
```

### Separación de responsabilidades entre apps

El proyecto está organizado en **5 aplicaciones Django** independientes, cada una con responsabilidades específicas:

#### 1. **`catalogo`** - Gestión de productos y contenido del sitio
**Responsabilidades:**
- Modelos: `Producto`, `Categoria`, `ImagenProducto`, `HeroHome`, `SeccionHome`, `PasoProceso`, `GaleriaTrabajo`, `PreguntaFrecuente`, `CTAFinal`, `ConfiguracionSitio`
- Vistas: Home, lista de catálogo, detalle de producto, galería completa, FAQ completa
- Templates: Páginas públicas relacionadas con productos
- Utilidades: Generación de mensajes WhatsApp, funciones SEO
- Template tags: Tags personalizados para WhatsApp

**Independencia:** Total. Puede funcionar sola con sus modelos y vistas.

#### 2. **`pedidos`** - Gestión de pedidos
**Responsabilidades:**
- Modelos: `Pedido`, `ConfiguracionPedido`
- Vistas: Crear pedido, confirmación de pedido
- Forms: `PedidoForm` con validación y honeypot anti-spam
- Templates: Formulario de pedido, página de confirmación
- Funcionalidades: Generación de mensajes WhatsApp prearmados, estados de pedido

**Dependencia:** Utiliza `catalogo.Producto` mediante ForeignKey, pero es opcional (permite pedidos sin producto específico).

#### 3. **`contacto`** - Consultas generales
**Responsabilidades:**
- Modelos: `Consulta`
- Vistas: Crear consulta, confirmación
- Forms: `ConsultaForm`
- Templates: Formulario de consultas, confirmación

**Independencia:** Total. No depende de otras apps.

#### 4. **`dashboard`** - Panel de gestión personalizado
**Responsabilidades:**
- Vistas: Dashboard principal, gestión de productos, gestión de pedidos, configuración del sitio
- Templates: Interface administrativa simplificada y amigable
- Funcionalidades: CRUD de productos simplificado, actualización de estados de pedidos, estadísticas

**Dependencia:** Utiliza modelos de `catalogo` y `pedidos`, pero no define modelos propios. Es una capa de presentación sobre los datos.

#### 5. **`accounts`** - Autenticación extendida
**Responsabilidades:**
- Extensión del sistema de autenticación de Django
- Personalización de vistas de login si es necesario

**Dependencia:** Utiliza `django.contrib.auth` nativo.

### Cómo se maneja frontend vs backend

El proyecto utiliza un enfoque **híbrido** con separación clara de responsabilidades:

#### Backend (Django)

- **Lógica de negocio**: Todas las reglas de negocio, validaciones y procesamiento están en Python/Django
- **Gestión de datos**: Models, migraciones, queries optimizadas
- **Seguridad**: CSRF, rate limiting, validaciones en el servidor
- **API implícita**: Las vistas renderizan templates, no exponen APIs REST (arquitectura tradicional Django)

#### Frontend (Templates Django + Tailwind CSS)

- **Templates Django**: Sistema de templates nativo de Django con herencia (`base.html`, bloques)
- **CSS Framework**: **Tailwind CSS** vía CDN (no se requiere build process)
- **JavaScript mínimo**: No hay framework JS (React/Vue). Solo JavaScript vanilla si es necesario para interacciones básicas
- **Responsive**: Diseño mobile-first usando utilidades de Tailwind

**Ventajas de este enfoque:**
- **Simplicidad**: No requiere procesos de build complejos
- **Rapidez de desarrollo**: Cambios en templates se reflejan inmediatamente
- **SEO friendly**: Todo el contenido es renderizado en el servidor
- **Mantenimiento**: Menos dependencias y herramientas que mantener

**Flujo de renderizado:**
```
Request → URL → View (Python) → Query DB → Context → Template → HTML Response
```

---

## 4. Tecnologías utilizadas (detalladas)

### Lenguaje principal

**Python 3.12.3**
- Lenguaje de programación utilizado para toda la lógica del backend
- Especificado en `runtime.txt` para asegurar consistencia en deployment
- Versión moderna que garantiza seguridad y rendimiento

### Framework web

**Django 6.0**
- Framework web completo de alto nivel
- Proporciona ORM, sistema de templates, autenticación, admin, seguridad
- Versión estable y actualizada con soporte a largo plazo

**Rol específico:**
- **ORM**: Gestión de base de datos mediante modelos Python (`models.py`)
- **Views**: Vistas basadas en funciones y clases (`ListView`, `DetailView`)
- **Templates**: Sistema de templates con herencia y tags personalizados
- **Middleware**: Stack de middleware para seguridad, sesiones, mensajes
- **Admin**: Panel de administración automático para todos los modelos
- **URL routing**: Sistema de URLs jerárquico y namespaced

### Base de datos

**Producción: PostgreSQL**
- Base de datos relacional robusta y escalable
- Configurada mediante variable de entorno `DATABASE_URL`
- Parseada usando `dj-database-url` para compatibilidad con múltiples plataformas
- Validación: El sistema bloquea SQLite en producción (`DEBUG=False`)

**Desarrollo: SQLite**
- Base de datos ligera para desarrollo local
- No requiere configuración adicional
- Automáticamente bloqueada si `DEBUG=False`

**Gestión:**
- Migraciones de Django para versionado del esquema
- Backup y restauración mediante herramientas estándar de PostgreSQL

### Almacenamiento de imágenes/media

**Sistema de archivos local** (configurable)
- Las imágenes se almacenan en el directorio `media/`
- Subdirectorios organizados:
  - `media/productos/`: Imágenes de productos
  - `media/secciones/`: Imágenes de secciones de la home
  - `media/hero/`: Imagen de fondo del hero
  - `media/logo/`: Logo de la marca
  - `media/galeria/`: Imágenes de la galería de trabajos

**Modelo utilizado:**
- `django.core.files.storage.FileSystemStorage` (default)
- Campo `ImageField` de Django con validación automática
- Procesamiento: **Pillow 10.4.0** para manipulación de imágenes

**Configuración para producción:**
- El sistema está preparado para usar servicios externos (ej: Cloudinary, AWS S3) cambiando `DEFAULT_FILE_STORAGE` en `settings.py`
- Actualmente configurado para almacenamiento local, adecuado para Railway o cualquier plataforma con persistencia de archivos

### Manejo de archivos estáticos

**Whitenoise 6.6.0**
- Middleware que sirve archivos estáticos directamente desde Django en producción
- Elimina la necesidad de un servidor web separado (nginx, Apache) para archivos estáticos
- Compresión automática de CSS/JS mediante `CompressedStaticFilesStorage`

**Configuración:**
- **MIDDLEWARE**: `whitenoise.middleware.WhiteNoiseMiddleware` después de `SecurityMiddleware`
- **STATICFILES_STORAGE**: `whitenoise.storage.CompressedStaticFilesStorage`
- **STATIC_ROOT**: `staticfiles/` (directorio donde se recolectan los estáticos con `collectstatic`)
- **STATICFILES_DIRS**: `static/` (directorio de origen de archivos estáticos)

**Archivos estáticos incluidos:**
- `static/css/style.css`: Estilos personalizados complementarios a Tailwind
- `static/admin/custom_admin.css`: Personalización del admin de Django

### Autenticación y permisos

**Sistema nativo de Django** (`django.contrib.auth`)
- Autenticación basada en usuarios estándar de Django
- Permisos: Solo usuarios autenticados pueden acceder al dashboard y admin
- Protección de vistas: Decorador `@login_required` en todas las vistas del dashboard

**Configuración de acceso:**
- **Admin de Django**: Solo superusuarios (`is_superuser=True`)
- **Dashboard personalizado**: Cualquier usuario autenticado
- **URLs públicas**: Sin restricción (catálogo, pedidos, contacto)

**Flujo de autenticación:**
- Login en `/accounts/login/` (template personalizado en `templates/registration/login.html`)
- Redirección post-login: `/dashboard/`
- Redirección post-logout: `/` (home)

### Admin y dashboard

#### Admin de Django (`/admin/`)

**Características:**
- Panel de administración completo y automático para todos los modelos
- Interfaz estándar de Django con personalizaciones en CSS
- Inlines: Gestión de imágenes de productos y secciones desde el mismo formulario
- Fieldsets: Organización lógica de campos en grupos
- List filters y search: Filtrado y búsqueda en todas las listas
- Prepopulated fields: Generación automática de slugs

**Modelos registrados:**
- `catalogo`: Categoria, Producto, ImagenProducto, SeccionHome, ImagenSeccion, HeroHome, PasoProceso, GaleriaTrabajo, PreguntaFrecuente, CTAFinal, ConfiguracionSitio
- `pedidos`: Pedido, ConfiguracionPedido
- `contacto`: Consulta

#### Dashboard personalizado (`/dashboard/`)

**Características:**
- Interfaz simplificada y amigable para operadores no técnicos
- Diseño consistente con el sitio público (mismo estilo visual)
- Funcionalidades principales:
  - Estadísticas: Pedidos nuevos, pedidos de la semana, productos activos
  - Lista de pedidos: Con filtros por estado, actualización de estados
  - Gestión de productos: Crear, editar, activar/desactivar productos
  - Configuración del sitio: Modificar WhatsApp, Instagram, textos, banner

**Ventajas vs Admin de Django:**
- Más intuitivo para usuarios no técnicos
- Enfoque en tareas operativas diarias
- Menos opciones = menos confusión

### Seguridad

El proyecto implementa múltiples capas de seguridad siguiendo las mejores prácticas de Django:

#### CSRF (Cross-Site Request Forgery)

- **Protección**: Middleware `CsrfViewMiddleware` activado globalmente
- **Tokens**: Tokens CSRF en todos los formularios
- **Configuración**: `CSRF_TRUSTED_ORIGINS` configurado mediante variable de entorno (requerido en producción)
- **Cookies**: `CSRF_COOKIE_SAMESITE='Lax'`, `CSRF_COOKIE_SECURE=True` en producción

#### Rate Limiting (Límite de peticiones)

**Librería: django-ratelimit 4.1.0**

- **Formulario de pedidos**: Máximo 5 peticiones POST por minuto por IP
- **Formulario de consultas**: Máximo 3 peticiones POST por minuto por IP
- **Propósito**: Prevenir abuso, spam y ataques de fuerza bruta
- **Implementación**: Decorador `@ratelimit` en vistas críticas

#### Headers de seguridad HTTP

Configurados automáticamente por Django en producción:

- **SECURE_SSL_REDIRECT**: Redirige HTTP a HTTPS
- **SESSION_COOKIE_SECURE**: Cookies de sesión solo por HTTPS
- **CSRF_COOKIE_SECURE**: Cookies CSRF solo por HTTPS
- **SECURE_HSTS_SECONDS**: 31536000 (1 año) - HTTP Strict Transport Security
- **SECURE_HSTS_INCLUDE_SUBDOMAINS**: HSTS aplica a subdominios
- **SECURE_HSTS_PRELOAD**: Permite inclusión en lista de preload de HSTS
- **SECURE_PROXY_SSL_HEADER**: Configurado para detectar HTTPS detrás de proxy (Railway, etc.)
- **X_FRAME_OPTIONS**: 'DENY' - Previene clickjacking
- **SECURE_BROWSER_XSS_FILTER**: Activa filtro XSS del navegador
- **SECURE_CONTENT_TYPE_NOSNIFF**: Previene MIME type sniffing
- **SECURE_REFERRER_POLICY**: 'strict-origin-when-cross-origin'

#### Validación de passwords

Validadores estándar de Django activados:
- Longitud mínima
- No solo numéricos
- No contraseñas comunes
- Validación de similitud con atributos del usuario

#### Protección contra spam

- **Honeypot**: Campo oculto `website` en formularios de pedidos que, si se completa, indica que es un bot
- **Validación en servidor**: Todas las validaciones se ejecutan en el backend, no solo en el frontend

### Mensajería por WhatsApp

**Integración no automatizada, basada en URLs**

El sistema no envía mensajes automáticamente, sino que genera URLs de WhatsApp Web/App con mensajes prearmados:

#### Generación de mensajes

**Para consultas de productos:**
- Función en `catalogo/utils.py`: `generar_mensaje_whatsapp(nombre_producto)`
- Template tag: `{% whatsapp_consulta producto %}` disponible en templates

**Para pedidos:**
- Método del modelo: `Pedido.get_mensaje_whatsapp()` genera mensaje estructurado con:
  - Nombre del cliente
  - Producto seleccionado (o "Personalizado")
  - Cantidad
  - Texto a grabar
  - Método de entrega
  - Zona/ciudad (si envío)
  - Fecha necesaria
  - Notas adicionales
  - WhatsApp del cliente

**Formato de URL:**
```
https://wa.me/{numero}?text={mensaje_url_encoded}
```

#### Configuración

- **Número de WhatsApp del sitio**: Configurable desde `ConfiguracionSitio` (usado en botón flotante)
- **Número de WhatsApp para pedidos**: Configurable desde `ConfiguracionPedido` (usado en confirmación de pedidos)
- **Variable de entorno**: `WHATSAPP_NUMBER` como fallback (usado en context processor)

#### Context Processors

Tres context processors personalizados inyectan datos en todos los templates:

1. **`whatsapp_number`**: Número de WhatsApp del sitio
2. **`google_analytics`**: ID de Google Analytics 4 (si está configurado)
3. **`configuracion_sitio`**: Objeto `ConfiguracionSitio` completo

### Variables de entorno

**Gestión: python-decouple 3.8**

Todas las configuraciones sensibles y específicas del entorno se gestionan mediante variables de entorno definidas en `.env` (desarrollo) o en el panel de Railway (producción).

**Variables requeridas:**

```
SECRET_KEY              # Clave secreta de Django (OBLIGATORIA)
DEBUG                   # True/False (default: False)
ALLOWED_HOSTS           # Lista separada por comas (ej: localhost,127.0.0.1,tu-dominio.com)
DATABASE_URL            # URL de PostgreSQL en producción (ej: postgresql://user:pass@host:port/db)
CSRF_TRUSTED_ORIGINS    # Orígenes permitidos para CSRF (ej: https://tu-dominio.com)
```

**Variables opcionales:**

```
WHATSAPP_NUMBER         # Número de WhatsApp (default: 5491112345678)
GA4_MEASUREMENT_ID      # ID de Google Analytics 4 (vacío = desactivado)
DJANGO_LOG_LEVEL        # Nivel de logging (default: INFO en dev, WARNING en prod)
RATELIMIT_ENABLE        # Activar rate limiting (default: True)
```

**Archivo de referencia:**
- `env.example`: Template con todas las variables documentadas

### Deploy target

**Railway** (configurado y listo)

El proyecto está configurado específicamente para deployment en Railway:

#### Configuración específica de Railway

**Procfile:**
```
web: gunicorn cami_zco.wsgi:application --bind 0.0.0.0:$PORT
```
- `gunicorn`: Servidor WSGI de producción
- `--bind 0.0.0.0:$PORT`: Binding requerido por Railway (puerto dinámico)

**Runtime:**
- `runtime.txt`: Especifica `python-3.12.3`

**Database:**
- Railway proporciona PostgreSQL automáticamente
- Variable `DATABASE_URL` se configura automáticamente al crear servicio de base de datos

**Static files:**
- Whitenoise sirve archivos estáticos (no requiere servicio adicional)
- `collectstatic` se ejecuta automáticamente en el build

**Variables de entorno:**
- Configurables desde el dashboard de Railway
- Persisten entre deploys

#### Dependencias de producción

Listadas en `requirements.txt`:

```
Django==6.0
psycopg[binary]==3.2.13          # Adaptador PostgreSQL (binario, compatible con Python 3.13)
python-decouple==3.8             # Gestión de variables de entorno
django-ratelimit==4.1.0          # Rate limiting
dj-database-url==3.0.1           # Parser de DATABASE_URL
gunicorn==21.2.0                 # Servidor WSGI
whitenoise==6.6.0                # Servir archivos estáticos
Pillow==10.4.0                   # Procesamiento de imágenes
```

**Nota sobre psycopg:**
- Se usa `psycopg[binary]` versión 3.2.13 (no `psycopg2`)
- Compatible con Python 3.12+ y evita problemas de compilación en Railway

---

## 5. Funcionalidades clave

### Catálogo de productos

**Características:**
- **Listado paginado**: Vista de todos los productos con paginación (si se implementa)
- **Filtrado por categorías**: Los productos pueden agruparse en categorías activas
- **Búsqueda**: Búsqueda por título y descripción (en admin)
- **Ordenamiento**: Por orden personalizado y fecha de creación
- **Productos destacados**: Campo `destacado` para mostrar productos en la home
- **Slugs SEO-friendly**: URLs amigables generadas automáticamente (ej: `/catalogo/vaso-grabado-personalizado/`)

**Modelo:**
- `Producto`: Título, descripción, categoría, precio (opcional), precio desde, tiempo estimado, activo, destacado, orden
- `Categoria`: Nombre, slug, descripción, orden, activa
- `ImagenProducto`: Relación uno-a-muchos con producto, orden, imagen principal

**Vistas:**
- `CatalogoListView`: Lista completa de productos activos
- `ProductoDetailView`: Detalle individual con todas las imágenes

### Página de detalle

**Características:**
- **Múltiples imágenes**: Galería de imágenes con imagen principal destacada
- **Información completa**: Título, descripción, precio (o "Consultar precio"), tiempo estimado
- **SEO optimizado**: Títulos y meta descriptions generados automáticamente
- **Open Graph**: Metadatos para compartir en redes sociales con imagen del producto
- **CTA directo**: Botón "Hacé tu pedido" que pre-selecciona el producto
- **WhatsApp rápido**: Botón de consulta rápida que genera mensaje prearmado

**Optimizaciones:**
- Queries optimizadas con `select_related` y `prefetch_related`
- Imágenes lazy-loaded (implementable en frontend)
- URLs canónicas mediante slug único

### Sistema de pedidos

**Flujo completo:**

1. **Inicio del pedido:**
   - Desde cualquier producto: `/pedir/<producto-slug>/` (producto pre-seleccionado)
   - Desde menú: `/pedir/` (producto opcional)

2. **Formulario estructurado:**
   - **Datos del cliente**: Nombre, WhatsApp
   - **Producto**: Selección del catálogo (opcional, puede ser "personalizado")
   - **Detalles del pedido**: Cantidad, texto a grabar (opcional pero recomendado)
   - **Logística**: Fecha necesaria (opcional), método de entrega (Retiro/Envío)
   - **Información adicional**: Zona/ciudad (si envío), notas generales
   - **Campo honeypot**: Protección anti-spam

3. **Validación:**
   - Validación en frontend (HTML5) y backend (Django forms)
   - Rate limiting: 5 pedidos por minuto por IP
   - CSRF protection en todos los envíos

4. **Confirmación:**
   - Página de confirmación con resumen del pedido
   - Link directo a WhatsApp con mensaje prearmado
   - Mensaje incluye toda la información estructurada

5. **Gestión posterior:**
   - Todos los pedidos quedan guardados en base de datos
   - Estados: Nuevo → Confirmado → En producción → Listo → Entregado
   - Notas internas para seguimiento del negocio

**Modelo `Pedido`:**
- Relación con producto (opcional)
- Campos de cliente y detalles
- Estado trackeable
- Timestamps automáticos
- Campo `notas_internas` visible solo en admin/dashboard

### Integración con WhatsApp

**No es una API automatizada**, sino una integración basada en URLs que facilita la comunicación:

**Tipos de integración:**

1. **Botón flotante** (todos los templates):
   - Fijo en la esquina inferior derecha
   - Link a WhatsApp con número configurable
   - Mensaje genérico o configurable

2. **Consulta rápida desde producto**:
   - Template tag `{% whatsapp_consulta producto %}`
   - Genera mensaje: "Hola! Vi este producto en tu web y quería consultarte: [Producto] [Link]"

3. **Confirmación de pedido**:
   - Mensaje estructurado con todos los datos del pedido
   - Generado por `Pedido.get_mensaje_whatsapp()`
   - URL-encoded para funcionar correctamente

4. **Configuración flexible**:
   - Número de WhatsApp configurable desde admin/dashboard
   - Mensajes personalizables
   - Sin dependencias externas (no requiere API de WhatsApp Business)

**Ventajas de este enfoque:**
- No requiere configuración de API de WhatsApp
- No tiene costos adicionales
- Funciona inmediatamente
- El negocio recibe el mensaje en su WhatsApp personal/business normal

### Panel de administración

**Dos niveles de administración:**

#### A. Dashboard personalizado (`/dashboard/`)

**Vista principal:**
- Estadísticas en tiempo real:
  - Pedidos nuevos (sin procesar)
  - Pedidos de la última semana
  - Productos activos
- Lista de pedidos recientes (últimos 5)

**Gestión de productos:**
- Lista de todos los productos con estado visual
- Crear producto: Formulario simplificado con subida de imagen principal
- Editar producto: Modificación de campos principales
- Activar/desactivar: Toggle rápido sin entrar a editar

**Gestión de pedidos:**
- Lista completa con filtros por estado
- Actualización de estado: Dropdown inline
- Visualización de detalles completos
- Edición de notas internas
- Link directo a WhatsApp del cliente desde cada pedido

**Configuración del sitio:**
- Número de WhatsApp del sitio
- Usuario de Instagram
- Texto del botón de pedidos
- Banner temporal (activar/desactivar con mensaje)

#### B. Admin de Django (`/admin/`)

**Gestión completa de contenido:**
- Todos los modelos con interfaz estándar de Django
- Gestión avanzada de imágenes (inlines)
- Categorías y organización
- Secciones de la home (Hero, Proceso, Galería, FAQ, CTA)
- Configuración avanzada del sitio

**Acceso:** Solo superusuarios

### Dashboard de gestión

El dashboard (`/dashboard/`) es una aplicación separada que proporciona una capa simplificada sobre los datos:

**Arquitectura:**
- No define modelos propios
- Usa modelos de `catalogo` y `pedidos`
- Vistas protegidas con `@login_required`
- Templates con diseño consistente con el sitio público

**Funcionalidades específicas:**
- Estadísticas calculadas en tiempo real
- Operaciones CRUD simplificadas (sin toda la complejidad del admin)
- Interfaz pensada para uso diario operativo
- Mensajes de éxito/error amigables

### Manejo de errores

**Páginas de error personalizadas:**

#### 404 - Página no encontrada

- Template: `templates/404.html`
- Diseño consistente con el sitio
- Mensaje amigable y botón de vuelta a home
- Se activa automáticamente cuando Django no encuentra una URL

#### 500 - Error del servidor

- Template: `templates/500.html`
- Diseño consistente con el sitio
- Mensaje de disculpas y contacto
- Se activa cuando ocurre una excepción no manejada

**Logging de errores:**

- **Archivo**: `logs/django.log` (si tiene permisos)
- **Consola**: Todos los errores también se registran en consola (visible en Railway logs)
- **Niveles configurados**:
  - Development: INFO
  - Production: WARNING (reduce ruido)
  - Errores de seguridad: Siempre WARNING
  - Errores de requests: ERROR

**Manejo graceful de permisos:**
- Si no puede crear directorio de logs, solo usa consola
- No falla el startup si hay problemas de permisos

### Optimización mobile

**Enfoque Mobile-First:**

1. **Diseño responsive con Tailwind CSS:**
   - Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
   - Navegación adaptativa: Menú hamburguesa en móvil (implementable)
   - Grids flexibles que se adaptan al ancho

2. **Viewport optimizado:**
   - Meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

3. **Formularios mobile-friendly:**
   - Inputs con `type="tel"` para WhatsApp (muestra teclado numérico en móvil)
   - Inputs con `type="date"` para fechas (muestra picker nativo)
   - Textareas con tamaño apropiado

4. **Botones táctiles:**
   - Tamaños mínimos para fácil toque (44x44px recomendado)
   - Espaciado adecuado entre elementos interactivos

5. **WhatsApp nativo:**
   - Links `wa.me` abren directamente la app de WhatsApp en móvil
   - Experiencia fluida sin salir del contexto

6. **Imágenes optimizadas:**
   - Uso de `ImageField` de Django con validación
   - Preparado para optimización adicional (compresión, WebP) si se requiere

**Testing recomendado:**
- Chrome DevTools device emulator
- Dispositivos reales iOS y Android
- Diferentes tamaños de pantalla

---

## 6. Nivel del proyecto

### Apto para producción

**Sí, el proyecto está listo para producción** con las siguientes consideraciones:

#### ✅ Aspectos completos y robustos

1. **Seguridad:**
   - Todas las configuraciones de seguridad de Django activadas en producción
   - CSRF, rate limiting, headers de seguridad
   - Validaciones en backend y frontend
   - Protección anti-spam (honeypot)

2. **Base de datos:**
   - Configuración para PostgreSQL en producción
   - Validación que bloquea SQLite en producción
   - Migraciones versionadas y organizadas

3. **Archivos estáticos:**
   - Whitenoise configurado correctamente
   - Compresión habilitada
   - `collectstatic` preparado para deployment

4. **Logging:**
   - Sistema de logging configurado
   - Manejo graceful de errores de permisos
   - Logs visibles en consola (Railway logs)

5. **Variables de entorno:**
   - Todas las configuraciones sensibles externalizadas
   - Validaciones en startup si faltan variables críticas
   - Warnings para configuraciones de producción incompletas

6. **Deployment:**
   - Procfile configurado para Railway
   - Runtime especificado
   - Dependencias actualizadas y compatibles

#### ⚠️ Consideraciones pre-deploy

**Variables de entorno requeridas en Railway:**
```
SECRET_KEY              # Generar una clave segura única
DEBUG                   # False
ALLOWED_HOSTS           # Dominio de Railway (ej: *.railway.app, tu-dominio.com)
DATABASE_URL            # Se configura automáticamente al crear servicio PostgreSQL
CSRF_TRUSTED_ORIGINS    # https://tu-dominio.railway.app
```

**Comandos post-deploy recomendados:**
```bash
python manage.py migrate          # Aplicar migraciones
python manage.py collectstatic    # Recolectar archivos estáticos (ya se hace en build)
python manage.py createsuperuser  # Crear usuario administrador
```

**Datos iniciales (opcionales):**
- Fixtures disponibles en `catalogo/fixtures/` y `pedidos/fixtures/`
- Cargar con: `python manage.py loaddata <fixture>`

#### 📋 Checklist pre-producción

- [x] Configurar todas las variables de entorno
- [x] Crear superusuario
- [x] Aplicar migraciones
- [ ] Cargar datos iniciales (productos de ejemplo, categorías, etc.)
- [ ] Configurar `ConfiguracionSitio` desde admin
- [ ] Configurar `ConfiguracionPedido` desde admin
- [ ] Subir imágenes de productos
- [ ] Configurar dominio personalizado (si aplica)
- [ ] Probar flujo completo: ver producto → hacer pedido → recibir en WhatsApp
- [ ] Verificar que los logs funcionen correctamente

### Escalabilidad

**Nivel actual: Escalable para pequeños/medianos negocios**

#### Capacidad estimada

**Productos:**
- Sin límite teórico (limitado por base de datos)
- Optimizado con índices en campos de búsqueda
- Queries eficientes con `select_related` y `prefetch_related`

**Pedidos:**
- Capacidad de miles de pedidos sin degradación notable
- Índices en campos de filtrado (estado, fecha)
- Ordenamiento eficiente

**Usuarios concurrentes:**
- Gunicorn con workers múltiples (configurable)
- Sin estado en sesiones (puede escalar horizontalmente)
- Base de datos PostgreSQL puede manejar cientos de conexiones simultáneas

#### Limitaciones actuales

1. **Almacenamiento de imágenes:**
   - Actualmente en sistema de archivos local
   - Railway tiene límites de espacio en disco
   - **Solución para escalar**: Migrar a S3, Cloudinary o similar

2. **Servidor único:**
   - Una instancia de Gunicorn
   - **Solución para escalar**: Múltiples instancias detrás de un load balancer

3. **Base de datos:**
   - PostgreSQL compartido (plan de Railway)
   - **Solución para escalar**: Base de datos dedicada, read replicas

#### Recomendaciones para escalar

**Corto plazo (hasta ~100 pedidos/mes):**
- Configuración actual es suficiente
- Monitorear uso de disco para imágenes

**Mediano plazo (100-500 pedidos/mes):**
- Migrar imágenes a servicio externo (Cloudinary, AWS S3)
- Aumentar workers de Gunicorn
- Configurar CDN para archivos estáticos (opcional)

**Largo plazo (500+ pedidos/mes):**
- Múltiples instancias de aplicación
- Base de datos dedicada con read replicas
- Cache con Redis para queries frecuentes
- Monitoreo y alertas (Sentry, etc.)

### Tipo de negocio que puede usarlo hoy

**Ideal para:**

1. **Emprendimientos individuales:**
   - Artesanos que personalizan productos
   - Talleres de grabado/impresión
   - Negocios unipersonales o familiares
   - **Volumen**: 10-50 pedidos/mes

2. **Pequeñas empresas:**
   - Tiendas de regalos personalizados
   - Servicios de personalización B2C
   - Negocios con 1-3 empleados
   - **Volumen**: 50-200 pedidos/mes

3. **Negocios en crecimiento:**
   - Startups en fase inicial
   - Negocios que quieren profesionalizar su presencia online
   - **Volumen**: Hasta ~300 pedidos/mes (con optimizaciones)

**No recomendado para (sin modificaciones):**

1. **E-commerce tradicional:**
   - Requiere pasarelas de pago
   - Carrito de compras
   - Checkout automático
   - Este proyecto está diseñado para pedidos asistidos, no venta directa

2. **Grandes volúmenes:**
   - Más de 500 pedidos/mes requeriría optimizaciones significativas
   - B2B con catálogos masivos

3. **Negocios que requieren:**
   - Inventario en tiempo real
   - Múltiples vendedores/tiendas
   - Integraciones complejas (ERP, contabilidad)
   - Multi-idioma avanzado

**Caso de uso perfecto:**
Un emprendedor que hace vasos grabados personalizados, recibe pedidos por WhatsApp e Instagram, y necesita:
- Mostrar su trabajo de forma profesional
- Facilitar que los clientes le envíen pedidos estructurados
- Organizar y seguir el estado de los pedidos
- Actualizar productos y contenido sin conocimientos técnicos

---

## 7. Stack resumido

### Backend

- **Lenguaje**: Python 3.12.3
- **Framework**: Django 6.0
- **ORM**: Django ORM (nativo)
- **Servidor WSGI**: Gunicorn 21.2.0
- **Base de datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Adaptador DB**: psycopg[binary] 3.2.13
- **Gestión de variables**: python-decouple 3.8
- **Parser DATABASE_URL**: dj-database-url 3.0.1

### Frontend

- **Templates**: Django Templates (sistema nativo)
- **CSS Framework**: Tailwind CSS (vía CDN)
- **CSS Personalizado**: CSS vanilla en `static/css/style.css`
- **JavaScript**: Vanilla JS (mínimo, solo si es necesario)
- **Responsive**: Mobile-first con Tailwind breakpoints

### Infraestructura

- **Plataforma de deploy**: Railway
- **Servidor de aplicación**: Gunicorn
- **Servidor de archivos estáticos**: Whitenoise 6.6.0
- **Procesamiento de imágenes**: Pillow 10.4.0
- **Runtime**: Python 3.12.3 (especificado en `runtime.txt`)
- **Proceso de build**: Automático en Railway (detecta `requirements.txt`, ejecuta `collectstatic`)

### Seguridad

- **CSRF Protection**: Django CsrfViewMiddleware
- **Rate Limiting**: django-ratelimit 4.1.0
- **Headers de seguridad**: Configurados automáticamente en producción
- **Validación de passwords**: Validadores estándar de Django
- **Anti-spam**: Campo honeypot en formularios
- **HTTPS**: Forzado en producción (SECURE_SSL_REDIRECT)

### Media

- **Almacenamiento**: Sistema de archivos local (`media/`)
- **Procesamiento**: Pillow 10.4.0
- **Campos**: Django ImageField
- **Organización**: Subdirectorios por tipo (productos/, secciones/, hero/, etc.)
- **Configuración futura**: Preparado para migrar a servicios externos (Cloudinary, S3)

### Utilidades y herramientas

- **Logging**: Sistema de logging nativo de Python/Django
- **Admin**: Django Admin (completo) + Dashboard personalizado (simplificado)
- **Migraciones**: Django Migrations (versionado de esquema)
- **Fixtures**: Datos iniciales en formato JSON
- **Template tags**: Tags personalizados para WhatsApp

---

## Conclusión

**cami.zco** es un sistema web completo, profesional y listo para producción, diseñado específicamente para negocios de productos personalizados que utilizan WhatsApp como canal principal de comunicación. 

El proyecto demuestra:

- **Arquitectura sólida**: Separación clara de responsabilidades, código organizado y mantenible
- **Seguridad robusta**: Múltiples capas de protección siguiendo mejores prácticas
- **Experiencia de usuario optimizada**: Proceso fluido desde la visualización hasta la confirmación de pedido
- **Facilidad de administración**: Dos niveles de admin (simplificado y avanzado) para diferentes necesidades
- **Escalabilidad adecuada**: Preparado para crecer con el negocio hasta cierto volumen
- **Deployment sencillo**: Configurado específicamente para Railway con documentación completa

Es una solución ideal para emprendedores y pequeñas empresas que buscan profesionalizar su presencia online sin la complejidad de un e-commerce tradicional, manteniendo el toque personal de la comunicación por WhatsApp.

---

**Documento generado para**: Presentación a clientes, onboarding de desarrolladores, documentación técnica del proyecto.  
**Última actualización**: 2025  
**Versión del proyecto**: Pre-deployment (listo para Railway)

