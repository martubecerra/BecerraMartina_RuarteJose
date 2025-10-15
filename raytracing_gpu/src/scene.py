# src/scene.py

from graphics import Graphics
from raytracer import RayTracer 
from raytracer import RayTracerGPU
import glm
import math
import numpy as np
from graphics import ComputeGraphics


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
        print("Scene Start!")

    def add_object(self, model, material):
        """Añade un objeto a la escena y crea su componente gráfico."""
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)

    def render(self):
        self.time += 0.01
        
        # Actualizar las matrices de vista y proyección en cada frame
        self.view = self.camera.get_view_matrix()
        self.projection = self.camera.get_perspective_matrix()

        for obj in self.objects:
            if (obj.animated):
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01

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

class RaySceneGPU(Scene):
    def __init__(self, ctx, camera, width, height, output_model, output_material):
        self.ctx = ctx
        self.camera = camera
        self.width = width
        self.height = height
        self.raytracer = None

        self.output_graphics = Graphics(ctx, output_model, output_material)
        self.raytracer = RayTracerGPU(self.ctx, self.camera, self.width, self.height, self.output_graphics)

        super().__init__(self.ctx, self.camera)

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = ComputeGraphics(self.ctx, model, material)

    def start(self):
        print("Start Raytracing!")
        self.primitives = []
        n = len(self.objects)
        self.models_f = np.zeros((n,16), dtype='f4')
        self.inv_f = np.zeros((n,16), dtype='f4')
        self.mats_f = np.zeros((n,4), dtype='f4')

        self._update_matrix()

        self._matrix_to_ssbo()

    def render(self):
        self.time += 0.01
        for obj in self.objects:
            if obj.animated:
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01

        if(self.raytracer is not None):
            self._update_matrix()
            self._matrix_to_ssbo()
            self.raytracer.run()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.width, self.height = width, height
        self.camera.aspect = width / height

    def _update_matrix(self):
        self.primitives = []

        for i, (name, graphics) in enumerate(self.graphics.items()):
            graphics.create_primitive(self.primitives)
            graphics.create_transformation_matrix(self.models_f, i)
            graphics.create_inverse_transformation_matrix(self.inv_f, i)
            graphics.create_material_matrix(self.mats_f, i)

    def _matrix_to_ssbo(self):
        self.raytracer.matrix_to_ssbo(self.models_f, 0)
        self.raytracer.matrix_to_ssbo(self.inv_f, 1)
        self.raytracer.matrix_to_ssbo(self.mats_f, 2)
        self.raytracer.primitive_to_ssbo(self.primitives, 3)