# src/scene.py

from graphics import Graphics
import glm
import math

class Scene:
    """
    Actúa como un contenedor que administra todos los objetos, la cámara
    y el ciclo de renderizado de la escena.
    """
    def __init__(self, ctx, camera):
        """
        Inicializa la escena con un contexto de OpenGL y una cámara.
        """
        self.ctx = ctx
        self.camera = camera
        self.objects = []      # Lista para guardar los objetos (ej: Cubo).
        self.graphics = {}     # Diccionario para guardar sus componentes gráficos (VBO, VAO).
        self.time = 0.00       # Tiempo simulado para animaciones.

    def add_object(self, obj, shader_program):
        """
        Añade un objeto a la escena y crea su representación gráfica.
        """
        self.objects.append(obj)
        # Asocia el objeto con sus datos gráficos usando su nombre como clave.
        self.graphics[obj.name] = Graphics(self.ctx, shader_program, obj.vertices, obj.indices)

    def render(self):
        """
        Dibuja todos los objetos de la escena. Este método se llama en cada frame.
        """

        # Incrementa el tiempo para que la animación avance.
        self.time += 0.01

        # Actualiza la rotación y posición de cada objeto en la escena.
        for obj in self.objects:
            obj.rotation.x += 0.8
            obj.rotation.y += 0.6
            # La función seno crea un suave movimiento de vaivén.
            obj.position.x += math.sin(self.time) * 0.01

        # Se obtienen las matrices de la cámara una sola vez por frame para mayor eficiencia.
        view_matrix = self.camera.get_view_matrix()
        projection_matrix = self.camera.get_perspective_matrix()

        # Itera sobre cada objeto para dibujarlo individualmente.
        for obj in self.objects:
            # Calcula la matriz MVP (Model-View-Projection) específica para este objeto.
            # Esta matriz combina la transformación del objeto, la cámara y la proyección.
            model_matrix = obj.get_model_matrix()
            mvp = projection_matrix * view_matrix * model_matrix
            
            # Obtiene el objeto gráfico correspondiente.
            graphics_obj = self.graphics[obj.name]
            
            # Envía la matriz MVP al shader para que la GPU pueda posicionar el objeto.
            graphics_obj.set_uniform('Mvp', mvp)
            
            # Ordena a la GPU que renderice la geometría del objeto.
            graphics_obj.vao.render()

    # Añadir el método para manejar el clic.
    def on_mouse_click(self, u, v):
        """Recibe las coordenadas del clic, genera un rayo y comprueba colisiones."""
        # Usar la cámara para generar el rayo.
        ray = self.camera.raycast(u, v)

        # Iterar sobre todos los objetos de la escena.
        for obj in self.objects:
            # Comprobar si el rayo intersecta el objeto.
            if obj.check_hit(ray.origin, ray.direction):
                # Si hay colisión, imprimir un mensaje en la consola.
                print(f"¡Golpeaste al objeto {obj.name}!")
    
    def on_resize(self, width, height):
        """
        Se ejecuta cuando la ventana cambia de tamaño para ajustar la vista.
        """
        # Ajusta el área de dibujo de OpenGL al nuevo tamaño de la ventana.
        self.ctx.viewport = (0, 0, width, height)
        # Actualiza la relación de aspecto de la cámara para evitar que la imagen se deforme.
        self.camera.aspect = width / height