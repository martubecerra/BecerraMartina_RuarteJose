# src/main.py

from window import Window
from shader_program import ShaderProgram
from cube import Cube
from camera import Camera
from scene import Scene

# Este es el script principal que une todos los componentes y ejecuta la aplicación.

# 1. Crear la ventana
# Se inicializa la ventana de Pyglet, que nos da un contexto de OpenGL para dibujar.
window = Window(800, 600, "Basic Graphic Engine")

# 2. Cargar los shaders
# Se crea un único programa de shaders que se usará para dibujar todos los objetos.
shader_program = ShaderProgram(window.ctx, 'shaders/basic.vert', 'shaders/basic.frag')

# 3. Configurar la cámara
# Se define el punto de vista desde el cual se observará la escena.
camera = Camera((0, 0, 6), (0, 0, 0), (0, 1, 0), 45, window.width / window.height, 0.1, 100.0)

# 4. Crear los objetos 3D
# Se crean las instancias de los cubos, definiendo su posición y rotación en el mundo.
cube1 = Cube((-2, 0, 0), (0, 45, 0), (1, 1, 1), name="Cube1")
cube2 = Cube((2, 0, 0), (0, 45, 0), (1, 1, 1), name="Cube2")

# 5. Crear la escena y añadir los objetos
# La escena actúa como un contenedor para todos los elementos que se van a renderizar.
scene = Scene(window.ctx, camera)
scene.add_object(cube1, shader_program)
scene.add_object(cube2, shader_program)

# 6. Cargar la escena en la ventana y ejecutar
# Se asigna la escena a la ventana y se inicia el bucle principal de la aplicación.
window.set_scene(scene)
window.run()