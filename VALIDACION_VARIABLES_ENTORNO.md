# Checklist de Validación: Variables de Entorno para Producción (Vercel)

**Fecha de validación:** $(date)  
**Contexto:** Deploy Django en Vercel con PostgreSQL (Neon) y Cloudinary

---

## 1. SECRET_KEY

### Estado Actual en Código
```python
SECRET_KEY = config('SECRET_KEY')  # Sin default: debe estar en .env
# ...
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no configurada. Debe estar definida en .env")
```

### Validación
- ✅ **Existe validación**: El código valida que exista y falla si falta
- ✅ **No está hardcodeada**: No hay default inseguro en el código
- ⚠️ **Validación de longitud**: El código NO valida la longitud mínima

### Configuración Requerida en Vercel
```
SECRET_KEY=<clave-generada-con-django>
```

### Cómo Generar
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Recomendaciones
- ✅ **Correcto**: La validación actual es suficiente (fail fast)
- ⚠️ **Mejora opcional**: Agregar validación de longitud mínima (50 caracteres)
- ✅ **Rotación**: Se puede rotar después del deploy sin problemas

### Estado Final
**✔ CORRECTO** - La configuración actual es segura. Solo asegurar que se genere una clave fuerte.

---

## 2. DEBUG

### Estado Actual en Código
```python
DEBUG = config('DEBUG', default=False, cast=bool)
```

### Validación
- ✅ **Default seguro**: `default=False` es correcto para producción
- ✅ **Cast a boolean**: `cast=bool` interpreta correctamente strings como "False" → False
- ✅ **Sin validación adicional**: No es necesaria, el default es seguro

### Configuración Requerida en Vercel
```
DEBUG=False
```

### Valores Aceptados
- `False` (recomendado, sin comillas)
- `false` (también funciona por `cast=bool`)
- `0` (también funciona por `cast=bool`)

### ⚠️ RIESGO DETECTADO
**Problema potencial**: Si alguien configura `DEBUG=True` o `DEBUG=true` en Vercel, la app funcionará en modo debug.

**Recomendación**: Agregar validación explícita en producción:
```python
if not DEBUG:
    # Validaciones de producción
else:
    # Solo permitir DEBUG=True en desarrollo local
    if os.environ.get('VERCEL'):
        raise ValueError("DEBUG=True no está permitido en Vercel (producción)")
```

### Estado Final
**✔ CORRECTO** - El default es seguro, pero se recomienda validación adicional para Vercel.

---

## 3. DATABASE_URL

### Estado Actual en Código
```python
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

# En producción, SQLite no está permitido
if not DEBUG and DATABASE_URL.startswith('sqlite'):
    raise ValueError("SQLite no está permitido en producción...")

# Validación adicional en producción
if not DEBUG:
    if not DATABASE_URL or DATABASE_URL.startswith('sqlite'):
        raise ValueError("DATABASE_URL debe estar configurada con PostgreSQL en producción...")
```

### Validación
- ✅ **Bloquea SQLite en producción**: Doble validación correcta
- ✅ **Valida formato**: Try/except al parsear con `dj-database-url`
- ⚠️ **No valida SSL explícitamente**: No verifica que tenga `sslmode=require`

### Configuración Requerida en Vercel
```
DATABASE_URL=postgresql://neondb_owner:password@ep-holy-dawn-a44cjqdg-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### Formato Correcto para Neon
```
postgresql://usuario:password@host:port/dbname?sslmode=require
```

### ⚠️ RIESGO DETECTADO
**Problema**: El código NO valida que `DATABASE_URL` incluya `sslmode=require` para conexiones seguras.

**Recomendación**: Agregar validación en producción:
```python
if not DEBUG:
    if 'sslmode=require' not in DATABASE_URL and DATABASE_URL.startswith('postgresql'):
        raise ValueError(
            "DATABASE_URL debe incluir 'sslmode=require' para conexiones seguras en producción"
        )
```

### Estado Final
**⚠️ REQUIERE ATENCIÓN** - Agregar validación de SSL mode para conexiones seguras.

---

## 4. ALLOWED_HOSTS

### Estado Actual en Código
```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
```

### Validación
- ✅ **Usa Csv()**: Interpreta correctamente valores separados por coma
- ⚠️ **Default inseguro para producción**: `localhost,127.0.0.1` no funciona en Vercel

### Configuración Requerida en Vercel
```
ALLOWED_HOSTS=tu-proyecto.vercel.app,*.vercel.app
```

### ❌ ERROR COMÚN DETECTADO
**Problema**: Muchos desarrolladores configuran:
```
ALLOWED_HOSTS=vercel.app  # ❌ INCORRECTO
```

**Correcto debe ser**:
```
ALLOWED_HOSTS=*.vercel.app  # ✅ CORRECTO
```

### Explicación Técnica
- Django requiere el **punto inicial** (`.`) para wildcard de subdominios
- `*.vercel.app` permite: `tu-proyecto.vercel.app`, `preview-abc123.vercel.app`, etc.
- `vercel.app` (sin punto) solo permite exactamente `vercel.app` (que no existe)

### Configuración Completa Recomendada
```
ALLOWED_HOSTS=tu-proyecto.vercel.app,*.vercel.app,tu-dominio.com,www.tu-dominio.com
```

### Estado Final
**⚠️ REQUIERE VALIDACIÓN** - Verificar que en Vercel esté configurado con `*.vercel.app` (con punto inicial).

---

## 5. CSRF_TRUSTED_ORIGINS

### Estado Actual en Código
```python
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
```

### Validación
- ✅ **Usa Csv()**: Interpreta correctamente valores separados por coma
- ⚠️ **Default vacío**: En producción debe estar configurado

### Configuración Requerida en Vercel
```
CSRF_TRUSTED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
```

### ❌ ERRORES COMUNES DETECTADOS

**Error 1: Sin esquema https://**
```
CSRF_TRUSTED_ORIGINS=tu-proyecto.vercel.app  # ❌ INCORRECTO
```
**Problema**: Django requiere el esquema completo (`https://`) para CSRF.

**Error 2: Sin wildcard**
```
CSRF_TRUSTED_ORIGINS=https://vercel.app  # ❌ INCORRECTO
```
**Problema**: No funciona con subdominios de Vercel.

**Error 3: Wildcard sin punto**
```
CSRF_TRUSTED_ORIGINS=https://*.vercel.app  # ⚠️ PARCIALMENTE CORRECTO
```
**Problema**: El wildcard `*` en CSRF_TRUSTED_ORIGINS tiene limitaciones. Mejor usar dominios específicos.

### Explicación Técnica
- **Esquema https:// obligatorio**: Django valida el origen completo (scheme + domain)
- **Wildcard limitado**: `https://*.vercel.app` funciona, pero es mejor ser explícito
- **Previews de Vercel**: Cada preview tiene un subdominio único, necesitas wildcard o listar todos

### Configuración Completa Recomendada
```
CSRF_TRUSTED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app,https://tu-dominio.com,https://www.tu-dominio.com
```

### ⚠️ MEJORA RECOMENDADA
Agregar validación en producción:
```python
if not DEBUG:
    if not CSRF_TRUSTED_ORIGINS:
        raise ValueError("CSRF_TRUSTED_ORIGINS debe estar configurado en producción")
    # Validar que todos tengan https://
    for origin in CSRF_TRUSTED_ORIGINS:
        if not origin.startswith('https://'):
            raise ValueError(f"CSRF_TRUSTED_ORIGINS debe usar https://: {origin}")
```

### Estado Final
**⚠️ REQUIERE VALIDACIÓN** - Verificar que en Vercel esté configurado con `https://` y wildcard correcto.

---

## 6. Variables de Cloudinary

### Estado Actual en Código
```python
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')  # Sin default
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')  # Sin default
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')  # Sin default

# ...
if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise ValueError("Variables de Cloudinary no configuradas...")
```

### Validación
- ✅ **Sin defaults**: Todas requieren configuración explícita
- ✅ **Fail fast**: Valida al inicio y falla si falta alguna
- ✅ **Validación completa**: Verifica las 3 variables requeridas

### Configuración Requerida en Vercel
```
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### Estado Final
**✔ CORRECTO** - La validación es completa y segura. Solo asegurar que las 3 variables estén configuradas en Vercel.

---

## Resumen Ejecutivo

### ✅ Variables Correctamente Configuradas
1. **SECRET_KEY** - Validación correcta, fail fast
2. **Cloudinary (3 variables)** - Validación completa, fail fast

### ⚠️ Variables que Requieren Atención
1. **DEBUG** - Default seguro, pero falta validación explícita para Vercel
2. **DATABASE_URL** - Falta validación de `sslmode=require`
3. **ALLOWED_HOSTS** - Requiere verificar formato `*.vercel.app` (con punto)
4. **CSRF_TRUSTED_ORIGINS** - Requiere verificar formato `https://*.vercel.app`

### 🔧 Cambios Exactos a Aplicar en Vercel

#### Variables REQUERIDAS (configurar en Vercel Dashboard)

```
SECRET_KEY=<generar-con-comando-django>
DEBUG=False
ALLOWED_HOSTS=tu-proyecto.vercel.app,*.vercel.app
CSRF_TRUSTED_ORIGINS=https://tu-proyecto.vercel.app,https://*.vercel.app
DATABASE_URL=postgresql://usuario:password@host:port/dbname?sslmode=require
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

#### Variables OPCIONALES
```
WHATSAPP_NUMBER=5491112345678
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
```

### ⚠️ Puntos Críticos a Verificar Antes del Deploy

1. **ALLOWED_HOSTS debe tener `*.vercel.app`** (con punto inicial)
   - ❌ Incorrecto: `vercel.app`
   - ✅ Correcto: `*.vercel.app`

2. **CSRF_TRUSTED_ORIGINS debe tener `https://` y wildcard**
   - ❌ Incorrecto: `tu-proyecto.vercel.app`
   - ❌ Incorrecto: `https://vercel.app`
   - ✅ Correcto: `https://tu-proyecto.vercel.app,https://*.vercel.app`

3. **DATABASE_URL debe incluir `sslmode=require`**
   - ❌ Incorrecto: `postgresql://user:pass@host/db`
   - ✅ Correcto: `postgresql://user:pass@host/db?sslmode=require`

4. **DEBUG debe ser exactamente `False`** (sin comillas)

### 📋 Checklist Pre-Deploy

- [ ] SECRET_KEY generada y configurada
- [ ] DEBUG=False configurado
- [ ] ALLOWED_HOSTS incluye `*.vercel.app` (con punto)
- [ ] CSRF_TRUSTED_ORIGINS incluye `https://*.vercel.app` (con https://)
- [ ] DATABASE_URL incluye `sslmode=require`
- [ ] CLOUDINARY_CLOUD_NAME configurado
- [ ] CLOUDINARY_API_KEY configurado
- [ ] CLOUDINARY_API_SECRET configurado
- [ ] Todas las variables configuradas para Production, Preview y Development en Vercel

---

## Mejoras Recomendadas en Código (Opcional)

### 1. Validación de SSL en DATABASE_URL
```python
if not DEBUG:
    if 'sslmode=require' not in DATABASE_URL and DATABASE_URL.startswith('postgresql'):
        raise ValueError("DATABASE_URL debe incluir 'sslmode=require' en producción")
```

### 2. Validación de DEBUG en Vercel
```python
if os.environ.get('VERCEL') and DEBUG:
    raise ValueError("DEBUG=True no está permitido en Vercel (producción)")
```

### 3. Validación de CSRF_TRUSTED_ORIGINS
```python
if not DEBUG:
    if not CSRF_TRUSTED_ORIGINS:
        raise ValueError("CSRF_TRUSTED_ORIGINS debe estar configurado en producción")
    for origin in CSRF_TRUSTED_ORIGINS:
        if not origin.startswith('https://'):
            raise ValueError(f"CSRF_TRUSTED_ORIGINS debe usar https://: {origin}")
```

---

**Fin del Checklist de Validación**

