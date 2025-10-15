# src/raytracer.py

from texture import Texture

class RayTracer:
    """Genera una imagen por CPU lanzando rayos a la escena."""
    def __init__(self, camera, width, height):
        self.camera = camera
        self.width = width
        self.height = height
        self.framebuffer = Texture(width=width, height=height, channels_amount=3)

        self.camera.set_sky_colors(top=(16, 150, 222), bottom=(181, 224, 247))

    def trace_ray(self, ray, objects):
        """Lanza un único rayo y determina su color."""
        for obj in objects:
            if obj.check_hit(ray.origin, ray.direction):
                return (255, 0, 0)  # Rojo para indicar colisión
        height = ray.direction.y
        return self.camera.get_sky_gradient(height)

    def render_frame(self, objects):
        """Recorre cada píxel de la pantalla para generar la imagen completa."""
        for y in range(self.height):
            for x in range(self.width):
                u = x / (self.width - 1)
                v = y / (self.height - 1)
                ray = self.camera.raycast(u, v)
                color = self.trace_ray(ray, objects)
                self.framebuffer.set_pixel(x, y, color)
    
    def get_texture(self):
        """Devuelve los datos de la imagen renderizada."""
        return self.framebuffer.image_data