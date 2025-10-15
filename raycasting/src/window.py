# src/window.py

import moderngl
import pyglet

class Window(pyglet.window.Window):
    """
    Gestiona la ventana principal de la aplicación usando Pyglet y el
    contexto de renderizado de ModernGL.
    """
    def __init__(self, width, height, title):
        """
        Inicializa la ventana de Pyglet y crea el contexto de ModernGL.
        """
        # Llama al constructor de la clase base (pyglet.window.Window) para crear la ventana.
        super().__init__(width, height, title, resizable=True)
        
        # Crea el contexto de ModernGL, que es el objeto principal para interactuar con la GPU.
        self.ctx = moderngl.create_context()
        
        # Prepara una variable para contener la escena que se va a renderizar.
        self.scene = None

    def set_scene(self, scene):
        """
        Asigna una escena a la ventana para ser dibujada.
        """
        self.scene = scene

    def on_draw(self):
        """
        Este es el "corazón" del bucle de renderizado. Pyglet lo llama automáticamente en cada frame.
        """
        # Limpia los buffers de la ventana (color y profundidad).
        self.clear()
        self.ctx.clear(0.08, 0.16, 0.18) # Limpia con un color de fondo oscuro.
        
        # Habilita el test de profundidad para que los objetos 3D se superpongan correctamente.
        self.ctx.enable(moderngl.DEPTH_TEST)
        
        # Si hay una escena cargada, le ordena que se renderice.
        if self.scene:
            self.scene.render()

    # Añadir el manejador de eventos del mouse.
    def on_mouse_press(self, x, y, button, modifiers):
        """Este método es llamado por Pyglet cuando se presiona un botón del mouse."""
        if self.scene is None:
            return

        # Convertir las coordenadas de píxeles (x, y) a coordenadas normalizadas [0, 1].
        u = x / self.width
        v = y / self.height

        # Delegar el evento a la escena para que maneje la lógica.
        self.scene.on_mouse_click(u, v)
    
    def on_resize(self, width, height):
        """
        Este método es llamado por Pyglet cada vez que el usuario cambia el tamaño de la ventana.
        """
        # Delega la lógica de redimensionado a la escena para que ajuste la cámara.
        if self.scene:
            self.scene.on_resize(width, height)

    def run(self):
        """
        Inicia el bucle principal de la aplicación de Pyglet.
        """
        # Este comando pone en marcha el gestor de eventos de Pyglet y empieza a llamar a on_draw().
        pyglet.app.run()