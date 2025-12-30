# 🚂 Guía de Deploy en Railway - cami.zco

## ✅ Estado Actual del Proyecto

### Archivos de Configuración Presentes
- ✅ `Procfile` - Configurado correctamente
- ✅ `requirements.txt` - Dependencias actualizadas
- ✅ `settings.py` - Configuración para producción
- ⚠️ `runtime.txt` - **FALTA** (Railway puede necesitarlo)

### Configuración Actual
- Python: 3.12.3 (local)
- Django: 6.0
- PostgreSQL: psycopg[binary]==3.2.13

---

## 🔧 Problemas Potenciales y Soluciones

### 1. **Falta `runtime.txt`** (RECOMENDADO)

Railway puede necesitar especificar la versión de Python explícitamente.

**Solución**: Crear archivo `runtime.txt` en la raíz con:
```
python-3.12.3
```

### 2. **Variables de Entorno en Railway**

Railway necesita estas variables configuradas en el dashboard:

**Variables CRÍTICAS:**
```
SECRET_KEY=<generar-nueva-clave>
DEBUG=False
ALLOWED_HOSTS=*.railway.app,tu-dominio.com
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://tu-dominio.com
DATABASE_URL=<Railway lo provee automáticamente si agregas PostgreSQL>
```

**Variables OPCIONALES:**
```
WHATSAPP_NUMBER=5491112345678
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
DJANGO_LOG_LEVEL=WARNING
```

### 3. **SECURE_SSL_REDIRECT puede causar problemas**

En `settings.py` línea 168, `SECURE_SSL_REDIRECT = True` puede causar loops infinitos si Railway no está configurado correctamente.

**Solución**: Comentar temporalmente o verificar que Railway esté detrás de un proxy HTTPS.

### 4. **Logging a archivo puede fallar**

El logging intenta escribir a `logs/django.log` que puede no tener permisos en Railway.

**Solución**: Ya está manejado en settings.py (líneas 237-248) con fallback a console.

---

## 📋 Checklist Pre-Deploy

### En Railway Dashboard:

1. **Crear nuevo proyecto**
   - Conectar repositorio Git
   - Railway detectará automáticamente el `Procfile`

2. **Agregar servicio PostgreSQL**
   - Railway creará automáticamente `DATABASE_URL`
   - No necesitas configurarla manualmente

3. **Configurar Variables de Entorno**
   - Ir a Variables tab
   - Agregar todas las variables críticas

4. **Generar SECRET_KEY**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Configurar ALLOWED_HOSTS**
   ```
   ALLOWED_HOSTS=*.railway.app,tu-dominio-custom.com
   ```

6. **Configurar CSRF_TRUSTED_ORIGINS**
   ```
   CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://tu-dominio-custom.com
   ```

---

## 🚀 Pasos de Deploy

### 1. Preparar el proyecto localmente

```bash
# Verificar que todo funciona
python manage.py check --deploy

# Verificar migraciones
python manage.py makemigrations --check --dry-run
```

### 2. Push a Git

```bash
git add .
git commit -m "Preparado para deploy en Railway"
git push origin main
```

### 3. En Railway

1. **Crear proyecto** desde el repositorio Git
2. **Agregar PostgreSQL** como servicio adicional
3. **Configurar variables de entorno** (ver arriba)
4. **Deploy automático** - Railway detectará el Procfile

### 4. Post-Deploy

Railway ejecutará automáticamente:
- `pip install -r requirements.txt`
- `gunicorn cami_zco.wsgi:application`

**PERO** necesitas ejecutar manualmente:
```bash
# En Railway CLI o en Deploy Logs, ejecutar:
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## ⚠️ Problemas Comunes

### Error: "No module named 'psycopg'"
- **Causa**: Railway no detectó correctamente las dependencias
- **Solución**: Verificar que `requirements.txt` esté en la raíz y tenga `psycopg[binary]==3.2.13`

### Error: "SECRET_KEY not configured"
- **Causa**: Variable de entorno no configurada
- **Solución**: Agregar `SECRET_KEY` en Variables de Railway

### Error: "DisallowedHost"
- **Causa**: `ALLOWED_HOSTS` no incluye el dominio de Railway
- **Solución**: Agregar `*.railway.app` a `ALLOWED_HOSTS`

### Error: "CSRF verification failed"
- **Causa**: `CSRF_TRUSTED_ORIGINS` no configurado
- **Solución**: Agregar `https://*.railway.app` a `CSRF_TRUSTED_ORIGINS`

### Error: "Database connection failed"
- **Causa**: PostgreSQL no agregado o `DATABASE_URL` incorrecta
- **Solución**: Agregar servicio PostgreSQL en Railway (se configura automáticamente)

### Error: "Static files not found"
- **Causa**: `collectstatic` no ejecutado
- **Solución**: Ejecutar `python manage.py collectstatic --noinput` en Railway

---

## 🔍 Verificación Post-Deploy

1. ✅ Home page carga: `https://tu-proyecto.railway.app`
2. ✅ Admin funciona: `https://tu-proyecto.railway.app/admin`
3. ✅ Dashboard funciona: `https://tu-proyecto.railway.app/dashboard`
4. ✅ Formularios funcionan (pedidos, consultas)
5. ✅ Imágenes cargan correctamente
6. ✅ Base de datos conectada (crear superusuario)

---

## 📝 Notas Importantes

1. **Railway detecta automáticamente** el `Procfile` y lo usa
2. **PostgreSQL se configura automáticamente** cuando agregas el servicio
3. **Variables de entorno** son críticas - sin ellas el deploy fallará
4. **Migraciones y collectstatic** deben ejecutarse manualmente la primera vez
5. **SECURE_SSL_REDIRECT** puede causar problemas - verificar logs si hay loops

---

## 🆘 Si el Deploy Sigue Fallando

1. **Revisar logs en Railway**: Ver qué error específico aparece
2. **Verificar variables de entorno**: Todas las críticas deben estar configuradas
3. **Verificar que PostgreSQL esté agregado**: Debe aparecer como servicio separado
4. **Revisar build logs**: Ver si `pip install` falla
5. **Verificar Procfile**: Debe estar en la raíz y tener el formato correcto

---

**Última actualización**: Pre-deploy Railway
**Estado**: Listo para deploy con las configuraciones correctas

