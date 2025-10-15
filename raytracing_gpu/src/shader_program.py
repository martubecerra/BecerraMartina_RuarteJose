# src/shader_program.py

from moderngl import Attribute, Uniform
import glm

class ShaderProgram:
    """
    Gestiona la carga, compilación y acceso a los shaders (vertex y fragment).
    En esta versión, detecta automáticamente los atributos y uniforms del shader.
    """
    def __init__(self, ctx, vertex_shader_path, fragment_shader_path):
        """
        Lee los archivos de shader, los compila y realiza una introspección
        para identificar sus atributos y uniforms.
        """
        with open(vertex_shader_path) as file:
            vertex_shader = file.read()
        with open(fragment_shader_path) as file:
            fragment_shader = file.read()
        
        # Compila y enlaza los shaders en un programa ejecutable en la GPU.
        self.prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # Introspección del Shader
        # Listas para almacenar los nombres de los atributos y uniforms encontrados.
        attributes = []
        uniforms = []
        
        # Itera sobre todos los "miembros" que expone el programa de shader compilado. 
        for name in self.prog:
            member = self.prog[name]
            if type(member) is Attribute:
                attributes.append(name)
            if type(member) is Uniform:
                uniforms.append(name)
                
        # Guarda las listas de nombres para uso futuro.
        self.attributes = list(attributes)
        self.uniforms = uniforms
            
    def set_uniform(self, name, value):
        """
        Envía datos desde Python a una variable 'uniform' dentro del shader,
        manejando diferentes tipos de datos. 
        """
        
        if name in self.uniforms:
            uniform = self.prog[name]
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"):
                uniform.value = value


class ComputeShaderProgram:
    def __init__(self, ctx, compute_shader_path):
        with open(compute_shader_path) as file:
            compute_source = file.read()
        self.prog = ctx.compute_shader(compute_source)

        uniforms = []
        for name in self.prog:
            member = self.prog[name]
            if type(member) is Uniform:
                uniforms.append(name)
        self.uniforms = uniforms

    def set_uniform(self, name, value):
        if name in self.uniforms:
            uniform = self.prog[name]
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"):
                uniform.value = value

    def run(self, groups_x, groups_y, groups_z=1):                                  
        self.prog.run(group_x=groups_x, group_y=groups_y, group_z=groups_z)
    


