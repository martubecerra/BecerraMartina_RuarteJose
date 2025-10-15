# src/ray.py

import glm

class Ray:
    """
    Representa un rayo en el espacio 3D, definido por un origen y una dirección.
    """
    def __init__(self, origin=(0, 0, 0), direction=(0, 0, 1)):
        # El origen es el punto de partida del rayo.
        self._origin = glm.vec3(*origin)
        # La dirección es un vector unitario (longitud 1) que indica hacia dónde apunta.
        self._direction = glm.normalize(glm.vec3(*direction))

    @property
    def origin(self) -> glm.vec3:
        return self._origin

    @property
    def direction(self) -> glm.vec3:
        return self._direction