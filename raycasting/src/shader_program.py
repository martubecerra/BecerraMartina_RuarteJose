# src/shader_program.py

class ShaderProgram:
    """
    Gestiona la carga y compilación de los archivos de shader (vertex y fragment)
    para que la GPU pueda utilizarlos.
    """
    def __init__(self, ctx, vertex_shader_path, fragment_shader_path):
        """
        Lee los archivos de shader desde el disco y los compila en un programa de GPU.
        """
        # Abre y lee el código fuente del vertex shader.
        with open(vertex_shader_path, 'r') as file:
            vertex_shader = file.read()
        
        # Abre y lee el código fuente del fragment shader.
        with open(fragment_shader_path, 'r') as file:
            fragment_shader = file.read()
        
        # ModernGL compila y enlaza ambos shaders en un solo programa ejecutable en la GPU.
        self.prog = ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )

    def set_uniform(self, name, value):
        """
        Envía datos desde Python a una variable 'uniform' dentro del shader.
        
        Las 'uniforms' son variables globales en los shaders que permiten pasar datos
        (como matrices de transformación, colores, etc.) desde la CPU a la GPU.
        """
        try:
            # Busca la uniform por su nombre en el shader y escribe el valor.
            self.prog[name].write(value.to_bytes())
        except KeyError:
            # Es una buena práctica advertir si una uniform no se encuentra, para facilitar la depuración.
            print(f"Advertencia: La uniform '{name}' no fue encontrada en el shader.")