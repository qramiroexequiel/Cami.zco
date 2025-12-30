# cami.zco – Pinturas y grabados

## 📋 Descripción

cami.zco es una plataforma web profesional diseñada para la gestión y venta de pinturas y grabados personalizados. El sistema permite a los clientes navegar un catálogo de productos, realizar pedidos personalizados y hacer consultas, mientras que la administradora gestiona productos, pedidos y consultas desde un panel de control intuitivo.

## ✨ Características Principales

### Público
- **Landing Page** con hero section, sección "Cómo funciona", galería de trabajos reales, FAQ y CTAs estratégicos
- **Catálogo de productos** con filtrado por categorías, paginación y diseño mobile-first
- **Detalle de producto** con galería de imágenes, descripción completa y CTA directo al formulario
- **Formulario de pedido** optimizado para conversión con validación server-side
- **Formulario de consultas** para contacto directo
- **Botón flotante de WhatsApp** siempre visible

### Panel Administrativo
- **CRUD completo de productos** con gestión de categorías
- **Subida de imágenes** mediante Cloudinary
- **Gestión de pedidos** con cambio de estados (Nuevo/Confirmado/En producción/Listo/Entregado)
- **Visualización de consultas** con marcado de leídas
- **Exportación de pedidos a CSV** para análisis y seguimiento

## 🛠️ Stack Tecnológico

- **Backend**: Django 6.0
- **Base de datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Almacenamiento de imágenes**: Cloudinary
- **Frontend**: Templates Django + Tailwind CSS (CDN)
- **Deploy**: Vercel
- **Seguridad**: CSRF protection, rate limiting, validaciones server-side

## 📁 Estructura del Proyecto

```
cami.zco/
├── cami_zco/                  # Proyecto Django principal
│   ├── settings.py          # Configuración con variables de entorno
│   ├── urls.py              # URLs principales
│   └── context_processors.py
├── catalogo/                 # App de productos
│   ├── models.py            # Producto, Categoria, ImagenProducto
│   ├── views.py             # Home, lista, detalle
│   ├── admin.py             # Panel admin de productos
│   └── fixtures/            # Datos de ejemplo
├── pedidos/                  # App de pedidos
│   ├── models.py            # Pedido con estados
│   ├── views.py             # Crear pedido, confirmación
│   ├── forms.py             # Formulario con validación
│   └── admin.py             # Gestión y exportación CSV
├── contacto/                 # App de consultas
│   ├── models.py            # Consulta
│   ├── views.py             # Crear consulta
│   └── admin.py             # Visualización de consultas
├── dashboard/                # Panel de administración personalizado
├── accounts/                 # App de autenticación
├── templates/                # Templates HTML
├── static/                  # CSS y archivos estáticos
├── vercel.json              # Configuración Vercel
└── requirements.txt         # Dependencias Python
```

## 🚀 Setup Local

### Prerrequisitos
- Python 3.12+
- pip
- (Opcional) PostgreSQL para producción local

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repo-url>
cd cami.zco
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus valores
```

5. **Aplicar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Cargar datos de ejemplo (opcional)**
```bash
python manage.py loaddata catalogo/fixtures/productos_ejemplo.json
```

8. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

El sitio estará disponible en `http://localhost:8000` y el dashboard en `http://localhost:8000/dashboard`

## 🌐 Deploy en Vercel

### Prerrequisitos
- Cuenta en Vercel
- Base de datos PostgreSQL (Neon o Supabase)
- Cuenta en Cloudinary

### Pasos

1. **Preparar el proyecto**
```bash
# Asegurarse de que todos los archivos estén commiteados
git add .
git commit -m "Preparado para deploy"
```

2. **Conectar con Vercel**
```bash
npm i -g vercel
vercel login
vercel
```

3. **Configurar variables de entorno en Vercel**

En el dashboard de Vercel (Settings → Environment Variables), agregar las siguientes variables:

**Variables REQUERIDAS (la app fallará sin estas):**

```
SECRET_KEY=tu-secret-key-generado
# Generar con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

DEBUG=False
# IMPORTANTE: Debe ser False en producción

ALLOWED_HOSTS=tu-proyecto.vercel.app,*.vercel.app
# IMPORTANTE: NO incluir protocolos (https://) en ALLOWED_HOSTS
# Incluir el dominio de Vercel y wildcard para previews
# Si tienes dominio personalizado: tu-dominio.com,www.tu-dominio.com
# El código automáticamente remueve protocolos si están presentes

CSRF_TRUSTED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
# IMPORTANTE: DEBE incluir https:// en CSRF_TRUSTED_ORIGINS
# URLs con https:// para CSRF protection
# Si tienes dominio personalizado: https://tu-dominio.com,https://www.tu-dominio.com
# El código automáticamente agrega https:// si falta

DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require
# Connection string de Neon o Supabase PostgreSQL
# Formato: postgresql://usuario:password@host:port/dbname?sslmode=require

CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
# Credenciales de Cloudinary para almacenamiento de imágenes
```

**Variables OPCIONALES:**

```
WHATSAPP_NUMBER=5491112345678
# Número de WhatsApp para el botón flotante (formato: 5491112345678)

GA4_MEASUREMENT_ID=G-XXXXXXXXXX
# Google Analytics 4 Measurement ID (opcional)
```

**Notas importantes:**
- Todas las variables deben configurarse para los ambientes: Production, Preview y Development
- Los dominios `*.vercel.app` son necesarios para que funcionen los previews de Vercel
- Si usas dominio personalizado, agregarlo también a `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`

4. **Configurar base de datos**

Si usas Neon:
- Crear proyecto en [Neon](https://neon.tech)
- Copiar la connection string y agregarla como `DATABASE_URL`

Si usas Supabase:
- Crear proyecto en [Supabase](https://supabase.com)
- Ir a Settings > Database > Connection string
- Copiar y agregar como `DATABASE_URL`

5. **Ejecutar migraciones**

Vercel ejecutará automáticamente las migraciones en el build, pero puedes hacerlo manualmente:

```bash
vercel env pull .env.production
python manage.py migrate
```

6. **Crear superusuario en producción**

Usar la consola de Vercel o conectarse directamente a la base de datos.

### Configuración de Build en Vercel

Vercel detectará automáticamente Django y usará `@vercel/python`. El archivo `vercel.json` ya está configurado.

## 📸 Screenshots

### Landing Page
![Landing Page](screenshots/landing.png)

### Catálogo
![Catálogo](screenshots/catalogo.png)

### Panel Admin
![Panel Admin](screenshots/admin.png)

*Nota: Agregar screenshots reales después del deploy*

## 🔒 Seguridad

- ✅ CSRF protection activado
- ✅ Validaciones server-side en todos los formularios
- ✅ Rate limiting en formularios (5 pedidos/min, 3 consultas/min)
- ✅ Variables sensibles en `.env`, nunca hardcodeadas
- ✅ Escaping automático en templates
- ✅ Headers de seguridad configurados

## 📝 Notas de Desarrollo

### Agregar nuevos productos
1. Ir a `/dashboard/productos/`
2. Completar información básica
3. Subir imágenes usando Cloudinary
4. Marcar como "destacado" para que aparezca en la home

### Cambiar estados de pedidos
1. Ir a `/dashboard/pedidos/`
2. Seleccionar pedidos y cambiar estado desde la lista
3. Exportar a CSV para análisis

### Personalizar diseño
- Editar `templates/base.html` para cambios globales
- Modificar `static/css/style.css` para estilos personalizados
- Los templates usan Tailwind CSS via CDN

## 🤝 Contribuciones

Este es un proyecto MVP. Para mejoras futuras:
- Sistema de autenticación para clientes
- Carrito de compras
- Integración con pasarelas de pago
- Notificaciones por email
- Dashboard con métricas

## 📄 Licencia

Proyecto privado - Todos los derechos reservados

## 👤 Contacto

Para consultas sobre el proyecto, contactar al desarrollador.

---
