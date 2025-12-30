# Checklist de Deploy - cami.zco

Este documento contiene los pasos necesarios para desplegar el proyecto en producción.

## Variables de Entorno Requeridas

### Variables CRÍTICAS (la app fallará sin estas):

```bash
SECRET_KEY=<generar-con-comando-abajo>
DEBUG=False
ALLOWED_HOSTS=tu-proyecto.vercel.app,*.vercel.app
CSRF_TRUSTED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require
```

### Variables OPCIONALES:

```bash
WHATSAPP_NUMBER=5491112345678
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
DJANGO_LOG_LEVEL=WARNING
```

## Generar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Comandos para Setup Local

### 1. Clonar y configurar entorno

```bash
git clone <repo-url>
cd cami.zco
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno local

Crear archivo `.env` en la raíz del proyecto:

```bash
SECRET_KEY=tu-secret-key-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
DATABASE_URL=sqlite:///db.sqlite3
```

### 3. Aplicar migraciones

```bash
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

### 5. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

## Comandos para Producción (Vercel)

### 1. Pre-deploy checks

```bash
python manage.py check
python manage.py check --deploy
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
```

### 2. Configurar variables en Vercel

1. Ir a Settings → Environment Variables
2. Agregar todas las variables requeridas
3. Configurar para Production, Preview y Development

### 3. Build y deploy

Vercel ejecutará automáticamente:
- `pip install -r requirements.txt`
- `python manage.py migrate` (si está configurado en vercel.json)
- `python manage.py collectstatic`

### 4. Verificar deploy

1. Acceder a la URL de producción
2. Verificar que el sitio carga correctamente
3. Probar formularios (pedidos, consultas)
4. Verificar enlaces de WhatsApp
5. Acceder al dashboard (`/dashboard/`)
6. Verificar carga de imágenes

## Pasos de Verificación Post-Deploy

### ✅ Funcionalidad Pública

- [ ] Home page carga correctamente
- [ ] Catálogo de productos visible
- [ ] Detalle de producto funciona
- [ ] Formulario de pedido funciona
- [ ] Formulario de consulta funciona
- [ ] Enlaces de WhatsApp funcionan
- [ ] Botón flotante de WhatsApp visible
- [ ] Imágenes se cargan correctamente

### ✅ Dashboard y Admin

- [ ] Login al dashboard funciona (`/dashboard/`)
- [ ] Lista de productos accesible
- [ ] Crear/editar productos funciona
- [ ] Lista de pedidos accesible
- [ ] Cambiar estado de pedidos funciona
- [ ] Configuración del sitio accesible
- [ ] Admin Django accesible (`/admin/`)

### ✅ Seguridad

- [ ] HTTPS funciona correctamente
- [ ] Headers de seguridad activos
- [ ] CSRF protection funcionando
- [ ] Rate limiting activo en formularios
- [ ] Dashboard requiere autenticación

### ✅ Errores

- [ ] Página 404 personalizada funciona
- [ ] Página 500 personalizada funciona
- [ ] Logs de errores funcionando

## Troubleshooting

### Error: SECRET_KEY no configurada

- Verificar que la variable esté en Vercel
- Regenerar SECRET_KEY si es necesario

### Error: DATABASE_URL no válida

- Verificar formato: `postgresql://user:pass@host:port/db?sslmode=require`
- Verificar que la base de datos esté accesible

### Error: ALLOWED_HOSTS

- Agregar dominio de Vercel: `*.vercel.app`
- Si hay dominio personalizado, agregarlo también

### Error: Static files no cargan

- Verificar que `collectstatic` se ejecutó
- Verificar configuración de WhiteNoise
- Verificar STATIC_ROOT y STATIC_URL

### Error: Migraciones pendientes

- Ejecutar: `python manage.py migrate`
- Verificar que no haya conflictos

## Notas Importantes

1. **Nunca** commitear el archivo `.env` con valores reales
2. **Siempre** usar `DEBUG=False` en producción
3. **Siempre** usar PostgreSQL en producción (no SQLite)
4. **Verificar** que todas las variables estén configuradas antes del deploy
5. **Probar** todos los flujos después del deploy

## Comandos Útiles

```bash
# Verificar configuración
python manage.py check --deploy

# Ver migraciones pendientes
python manage.py makemigrations --check --dry-run

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Ver logs en producción (Vercel)
vercel logs

# Conectar a base de datos (si es necesario)
# Usar cliente PostgreSQL o herramienta de Neon/Supabase
```

---

**Última actualización**: Pre-deploy cleanup completado
**Estado**: Listo para producción

