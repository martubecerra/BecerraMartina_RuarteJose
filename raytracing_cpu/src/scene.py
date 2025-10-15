# src/scene.py

from graphics import Graphics
from raytracer import RayTracer
import glm
import math

class Scene:
    """
    Contenedor principal que administra los objetos, la cámara, la animación
    y el ciclo de renderizado, siguiendo la estructura exacta de la guía.
    """
    def __init__(self, ctx, camera):
        """Inicializa la escena con un contexto de OpenGL y una cámara."""
        self.ctx = ctx
        self.camera = camera
        self.objects = []
        self.graphics = {}
        self.time = 0.0
        
        # Inicializa las matrices de vista y proyección
        self.view = glm.lookAt(glm.vec3(0, 0, -5), glm.vec3(0), glm.vec3(0, 1, 0))
        self.projection = glm.perspective(glm.radians(45.0), camera.aspect, 0.1, 100.0)

    def start(self):
        """Se llama una vez cuando la escena está lista."""
        print("Scene Start!")

    def add_object(self, model, material):
        """Añade un objeto a la escena y crea su componente gráfico."""
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)

    def render(self):
        """
        En un único bucle, actualiza la animación de los objetos y renderiza por GPU
        aquellos que tienen un componente gráfico.
        """
        
        # Incrementa el tiempo para que la animación avance.
        self.time += 0.01

        # Itera sobre todos los objetos de la escena.
        for obj in self.objects:
            if (obj.name != "Sprite"):
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01

            # Renderiza el objeto usando los atributos self.projection y self.view.
            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].render({'Mvp': mvp})

    def on_mouse_click(self, u, v):
        """Maneja los clics para detectar colisiones."""
        ray = self.camera.raycast(u, v)
        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"¡Golpeaste al objeto {obj.name}!")
    
    def on_resize(self, width, height):
        """Ajusta la cámara y el viewport al cambiar el tamaño de la ventana."""
        self.camera.aspect = width / height
        self.ctx.viewport = (0, 0, width, height)
        # Actualiza la matriz de proyección con el nuevo aspect ratio
        self.projection = glm.perspective(glm.radians(45.0), self.camera.aspect, 0.1, 100.0)


class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.raytracer = RayTracer(camera, width, height)

    def start(self):
        print("RayScene: Renderizando frame en CPU... (puede tardar)")
        self.raytracer.render_frame(self.objects)
        if "Sprite" in self.graphics:
            self.graphics["Sprite"].update_texture("u_texture", self.raytracer.get_texture())
        print("RayScene: Renderizado completo.")

    def render(self):
        # Delega a la clase padre para dibujar el Quad y animar los cubos.
        super().render()

    def on_resize(self, width, height):
        # Re-renderiza la escena en la CPU si la ventana cambia de tamaño.
        super().on_resize(width, height)
        self.raytracer = RayTracer(self.camera, width, height)
        self.start()