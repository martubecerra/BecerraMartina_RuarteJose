# src/graphics.py

class Graphics:
    """
    Gestiona los objetos de bajo nivel de OpenGL (VBO, IBO, VAO)
    que son necesarios para que la GPU pueda dibujar una geometría.
    """
    def __init__(self, ctx, shader_program, vertices, indices):
        """
        Inicializa los buffers con la geometría y configura el VAO.
        """
        self.ctx = ctx
        self.shader_program = shader_program

        # VBO (Vertex Buffer Object): Almacena en la GPU los datos de los vértices (posición, color, etc.).
        self.vbo = ctx.buffer(vertices.tobytes())

        # IBO (Index Buffer Object): Almacena los índices que definen el orden de dibujo de los vértices.
        self.ibo = ctx.buffer(indices.tobytes())

        # VAO (Vertex Array Object): Es como una "receta" que le dice a la GPU cómo interpretar los datos
        # del VBO e IBO, conectándolos a las entradas ('in') del vertex shader.
        self.vao = ctx.vertex_array(
            shader_program.prog,
            [
                # Formato: '3f 3f' → dos atributos de 3 floats (xyz y rgb).
                # Nombres: 'in_pos', 'in_color' → nombres de las variables 'in' en el vertex shader.
                (self.vbo, '3f 3f', 'in_pos', 'in_color')
            ],
            index_buffer=self.ibo
        )

    def set_shader(self, shader_program):
        """
        Asigna un programa de shaders. 
        """
        self.shader_program = shader_program.prog

    def set_uniform(self, name, value):
        """
        Un método práctico para enviar datos a las variables 'uniform' del shader.
        """
        self.shader_program.set_uniform(name, value)