# Instrucciones para Gestionar Contenido Visual

## Sección "Nuestro Trabajo"

### Cómo editar el texto

1. Ir a **Admin Django** → **Catálogo** → **Secciones Home**
2. Buscar la sección "Nuestro Trabajo"
3. Hacer clic para editar
4. Modificar el **Título** y el **Texto** según necesites
5. Guardar cambios

### Cómo agregar/cambiar la imagen

1. En la misma página de edición de la sección "Nuestro Trabajo"
2. Bajar hasta la sección **"Imágenes de la sección"**
3. Para agregar una nueva imagen:
   - Hacer clic en "Agregar otra Imagen de Sección"
   - Subir la imagen (se guardará automáticamente en Cloudinary)
   - Completar el **Texto alternativo** (importante para accesibilidad)
   - Seleccionar el **Tipo** (Proceso de trabajo, Trabajo real, etc.)
   - Establecer el **Orden** (1 para la imagen principal)
   - Marcar como **Activa**
   - Guardar

4. Para cambiar la imagen principal:
   - Editar la imagen existente o agregar una nueva
   - Asegurarse de que tenga **Orden = 1** y esté **Activa**
   - Desactivar o eliminar la imagen anterior si ya no la necesitas

### Tipos de imágenes disponibles

- **Proceso de trabajo**: Manos grabando, herramientas, mesa de trabajo
- **Trabajo real**: Piezas terminadas, trabajos de clientes
- **Logo**: Logo de la marca
- **Persona trabajando**: Fotos tuyas trabajando (sin mostrar rostro si preferís)
- **Cliente**: Fotos de clientes (con permiso)
- **Evento**: Imágenes de eventos especiales
- **Temporada**: Imágenes estacionales
- **Otro**: Cualquier otra imagen

### Gestión independiente de imágenes

También puedes gestionar imágenes desde:
- **Admin Django** → **Catálogo** → **Imágenes de Secciones**

Aquí puedes:
- Ver todas las imágenes
- Editar o eliminar imágenes
- Cambiar el orden
- Activar/desactivar imágenes

## Notas importantes

- **La primera imagen activa con orden más bajo** será la que se muestre en la sección
- Las imágenes se optimizan automáticamente con Cloudinary
- El **texto alternativo** es importante para accesibilidad y SEO
- Puedes tener múltiples imágenes y cambiar cuál se muestra cambiando el orden
- Si desactivas una imagen, no se mostrará en el sitio pero se mantiene en la base de datos

## Futuras secciones

El sistema está preparado para agregar más secciones visuales en el futuro:
- Secciones de proceso
- Testimoniales con imágenes
- Galerías de trabajos
- Etc.

Todas se gestionan de la misma forma desde el panel de administración.

