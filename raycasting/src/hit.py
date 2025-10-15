# src/hit.py

import glm

class Hit:
    """
    Clase base para colisionadores. Ahora trabaja con una función que
    devuelve la matriz de modelo actualizada del objeto.
    """
    def __init__(self, get_model_matrix):
        # Guarda la función que obtiene la matriz, no la matriz en sí.
        self._model_matrix = get_model_matrix

    @property
    def model_matrix(self):
        # Al acceder a esta propiedad, se ejecuta la función y se obtiene la matriz más reciente.
        return self._model_matrix()

    @property
    def position(self):
        # La posición se extrae de la última columna de la matriz de modelo.
        m = self.model_matrix
        return glm.vec3(m[3].x, m[3].y, m[3].z)

    @property
    def scale(self):
        # La escala se calcula midiendo la longitud de los vectores base de la matriz.
        m = self.model_matrix
        return glm.vec3(
            glm.length(glm.vec3(m[0])),
            glm.length(glm.vec3(m[1])),
            glm.length(glm.vec3(m[2]))
        )

    def check_hit(self, origin, direction):
        raise NotImplementedError("Las subclases deben implementar este método.")

class HitBoxOBB(Hit):
    """
    Representa una caja de colisión orientada (OBB).
    Funciona transformando el rayo al espacio local del objeto.
    """
    def __init__(self, get_model_matrix):
        super().__init__(get_model_matrix)

    def check_hit(self, origin, direction):
        # Transformar el rayo de espacio de mundo a espacio local.
        inv_model = glm.inverse(self.model_matrix)
        local_origin = inv_model * glm.vec4(origin, 1.0)
        local_dir = inv_model * glm.vec4(direction, 0.0)

        local_origin = glm.vec3(local_origin)
        local_dir = glm.normalize(glm.vec3(local_dir))

        # Realizar el test de colisión AABB en el espacio local.
        # En su propio espacio, el objeto es un cubo perfecto de -1 a 1.
        min_bounds = glm.vec3(-1, -1, -1)
        max_bounds = glm.vec3(1, 1, 1)

        tmin = (min_bounds - local_origin) / local_dir
        tmax = (max_bounds - local_origin) / local_dir

        t1 = glm.min(tmin, tmax)
        t2 = glm.max(tmin, tmax)

        t_near = max(t1.x, t1.y, t1.z)
        t_far = min(t2.x, t2.y, t2.z)

        return t_near <= t_far and t_far >= 0