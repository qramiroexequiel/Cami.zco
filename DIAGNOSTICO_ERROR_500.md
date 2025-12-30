# Diagnóstico: Error 500 FUNCTION_INVOCATION_FAILED en Vercel

**Fecha:** $(date)  
**Contexto:** Django en Vercel serverless, error 500 al acceder a "/"  
**Build:** ✅ Exitoso  
**Deploy:** ✅ Sin errores  
**Runtime:** ❌ FUNCTION_INVOCATION_FAILED

---

## Análisis del Problema

### Punto MÁS Probable de Crash

**Archivo:** `cami_zco/settings.py`  
**Líneas:** 160-171 (Configuración de Cloudinary)  
**Problema:** Orden de inicialización y validación

### Explicación Técnica

El problema está en el **orden de ejecución** en `settings.py`:

```python
# Líneas 161-163: Se leen variables (sin default, pero pueden ser strings vacíos)
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')  # Puede ser ''
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')  # Puede ser ''
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')  # Puede ser ''

# Líneas 165-169: Se crea CLOUDINARY_STORAGE con valores potencialmente vacíos
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,  # Puede ser ''
    'API_KEY': CLOUDINARY_API_KEY,  # Puede ser ''
    'API_SECRET': CLOUDINARY_API_SECRET,  # Puede ser ''
}

# Línea 171: Se configura DEFAULT_FILE_STORAGE con Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ... (mucho código después) ...

# Líneas 285-289: VALIDACIÓN está AQUÍ, demasiado tarde
if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise ValueError("Variables de Cloudinary no configuradas...")
```

### Por Qué Rompe en Vercel

1. **En Vercel, si las variables no están configuradas**, `config()` retorna strings vacíos (`''`), no `None`
2. **`CLOUDINARY_STORAGE` se crea con valores vacíos** antes de la validación
3. **Django inicializa Cloudinary** con configuración inválida
4. **Cuando la vista `home()` ejecuta queries** que incluyen `CloudinaryField` (línea 19 de `home.html`: `producto.imagenes.first.imagen.url`), Cloudinary intenta acceder a la API con credenciales vacías
5. **Cloudinary falla silenciosamente o lanza excepción** que no se captura, causando el crash de la función serverless

### Evidencia

- La vista `home()` accede a `producto.imagenes.first.imagen.url` en el template
- `ImagenProducto` usa `CloudinaryField` que requiere configuración válida
- Las validaciones están **después** de la configuración de Cloudinary
- Si las variables están vacías, `CLOUDINARY_STORAGE` tiene valores inválidos pero la validación no se ejecuta hasta después

---

## Otros Problemas Potenciales (Menos Probables)

### 2. Queries a DB sin manejo de errores
**Archivo:** `catalogo/views.py`, función `home()`  
**Línea:** 14-57  
**Problema:** Si la DB no está conectada o hay timeout, las queries fallan sin try/except

**Probabilidad:** Media (menos probable porque el build pasa, lo que sugiere que la DB está configurada)

### 3. `prefetch_related` con `models.Prefetch` complejo
**Archivo:** `catalogo/views.py`, línea 32-37  
**Problema:** El `Prefetch` anidado puede fallar en serverless si hay problemas de conexión

**Probabilidad:** Baja (esto funcionaría si la DB está bien)

### 4. Validaciones que rompen el arranque
**Archivo:** `cami_zco/settings.py`, líneas 281-298  
**Problema:** Si alguna validación falla, rompe el arranque completo

**Probabilidad:** Media (pero el build pasa, así que las variables críticas probablemente están)

---

## Solución Propuesta

### Cambio Mínimo y Seguro

**Archivo:** `cami_zco/settings.py`  
**Ubicación:** Mover validación de Cloudinary ANTES de crear `CLOUDINARY_STORAGE`

**Cambio:**

```python
# ANTES (líneas 160-171):
# Cloudinary settings
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')  # Sin default
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')  # Sin default
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')  # Sin default

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ... (mucho código) ...

# Líneas 285-289: Validación aquí (demasiado tarde)
if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise ValueError("Variables de Cloudinary no configuradas...")

# DESPUÉS:
# Cloudinary settings
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')  # Sin default
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')  # Sin default
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')  # Sin default

# VALIDAR INMEDIATAMENTE después de leer (fail fast)
if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise ValueError(
        "Variables de Cloudinary no configuradas. "
        "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY y CLOUDINARY_API_SECRET deben estar en .env"
    )

# Solo crear CLOUDINARY_STORAGE si las variables son válidas
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ... (resto del código) ...

# Remover la validación duplicada de las líneas 285-289
```

### Por Qué Esta Solución Funciona

1. **Fail Fast**: Si las variables faltan, falla inmediatamente en startup, no en runtime
2. **Evita configuración inválida**: `CLOUDINARY_STORAGE` solo se crea con valores válidos
3. **Mensaje de error claro**: El error aparece en el build/deploy, no como 500 en runtime
4. **Mínimo cambio**: Solo mueve la validación, no cambia lógica

### Impacto

- ✅ **Sin breaking changes**: Solo cambia el orden de validación
- ✅ **Más seguro**: Falla en build si las variables faltan
- ✅ **Mensaje claro**: Error visible en logs de Vercel durante build
- ✅ **No afecta funcionalidad**: Si las variables están bien, funciona igual

---

## Verificación Adicional Recomendada

Si el problema persiste después de este cambio, verificar:

1. **Variables de entorno en Vercel**: Asegurar que `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY` y `CLOUDINARY_API_SECRET` estén configuradas y no vacías
2. **Logs de Vercel**: Revisar Function Logs en Vercel dashboard para ver el error exacto
3. **Conexión a DB**: Verificar que `DATABASE_URL` esté correcta y la DB esté accesible desde Vercel

---

## Resumen Ejecutivo

**Problema:** Cloudinary se configura con valores potencialmente vacíos antes de validar que las variables existan, causando crash en runtime cuando se accede a imágenes.

**Solución:** Mover validación de Cloudinary inmediatamente después de leer las variables, antes de crear `CLOUDINARY_STORAGE`.

**Archivo a modificar:** `cami_zco/settings.py` (líneas 160-171 y 285-289)

**Riesgo:** Mínimo (solo reordenamiento de código)

**Beneficio:** Fail fast en build en lugar de crash en runtime

