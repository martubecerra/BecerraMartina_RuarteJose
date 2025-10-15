# src/cube.py

import numpy as np
import glm
from hit import HitBoxOBB

class Cube:
    """
    Define la geometría de un cubo y sus transformaciones en el espacio (posición, rotación, escala).
    """
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), name="cube"):
        """
        Inicializa las propiedades de transformación del cubo y sus datos geométricos.
        """
        self.name = name
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        self.__colision = HitBoxOBB(get_model_matrix=lambda: self.get_model_matrix())
        
        # Array de vértices: 8 vértices, cada uno con 3 floats para posición (xyz) y 3 para color (rgb).
        self.vertices = np.array([
            # pos (x,y,z) # color (r,g,b)
            -1, -1,  1,   1, 0, 1,
             1, -1,  1,   0, 1, 1,
             1,  1,  1,   0, 0, 1,
            -1,  1,  1,   1, 1, 0,
            -1, -1, -1,   1, 0, 0,
             1, -1, -1,   0, 1, 0,
             1,  1, -1,   1, 1, 1,
            -1,  1, -1,   0, 0, 0,
        ], dtype='f4')
        
        # Array de índices: define cómo se conectan los vértices para formar 12 triángulos (6 caras).
        self.indices = np.array([
            0, 1, 2,   2, 3, 0,  # Cara frontal
            4, 5, 6,   6, 7, 4,  # Cara trasera
            3, 2, 6,   6, 7, 3,  # Cara superior
            0, 1, 5,   5, 4, 0,  # Cara inferior
            0, 3, 7,   7, 4, 0,  # Cara izquierda
            1, 2, 6,   6, 5, 1,  # Cara derecha
        ], dtype='i4')

    def check_hit(self, origin, direction):
        """Delega la comprobación de la colisión a su hitbox interna."""
        return self.__colision.check_hit(origin, direction)

    def get_model_matrix(self):
        """
        Calcula la matriz de modelo (Model Matrix).
        Esta matriz transforma los vértices del cubo desde su espacio local al espacio del mundo.
        """
        # Se parte de una matriz identidad (un objeto sin transformar).
        model = glm.mat4(1.0)
        
        # Se aplican las transformaciones en orden: Escala -> Rotación -> Traslación.
        # GLM las aplica en orden inverso, por lo que el código se escribe así:
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.scale)
        
        return model