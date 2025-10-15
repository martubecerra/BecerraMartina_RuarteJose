from ray import Ray
import glm

class Camera:
    def __init__(self, position, target, up, fov, aspect, near, far):
        self.position = glm.vec3(*position)
        self.target = glm.vec3(*target)
        self.up = glm.vec3(*up)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.__sky_color_top = None
        self.__sky_color_bottom = None

    def set_sky_colors(self, top, bottom):
        self.__sky_color_top = glm.vec3(*top)
        self.__sky_color_bottom = glm.vec3(*bottom)

    def get_sky_gradient(self, height):
        point = pow(0.5 * (height + 1.0), 1.5)
        return (1.0 - point) * self.__sky_color_bottom + point * self.__sky_color_top

    def get_view_matrix(self):
        """
        Calcula la matriz de vista (View Matrix).
        Esta matriz define la posición y orientación de la cámara en el mundo.
        """
        # glm.lookAt construye la matriz a partir de dónde está la cámara, a dónde mira y cuál es su "arriba".
        return glm.lookAt(self.position, self.target, self.up)

    def get_perspective_matrix(self):
        """
        Calcula la matriz de proyección (Projection Matrix).
        Esta matriz crea la ilusión de profundidad y perspectiva.
        """
        # glm.perspective necesita el campo de visión (fov) en radianes.
        return glm.perspective(glm.radians(self.fov), self.aspect, self.near, self.far)

    def raycast(self, u, v):
        """
        Genera un rayo desde la cámara a través de las coordenadas normalizadas (u, v) de la pantalla.
        """
        # Ajustar por campo de visión (FOV).
        fov_adjustment = glm.tan(glm.radians(self.fov) / 2)

        # Convertir coordenadas de pantalla [0, 1] a Coordenadas de Dispositivo Normalizado [-1, 1].
        ndc_x = (2 * u - 1) * self.aspect * fov_adjustment
        ndc_y = (2 * v - 1) * fov_adjustment

        # Dirección del rayo en el espacio de la cámara (siempre apunta hacia -Z).
        ray_dir_camera = glm.vec3(ndc_x, ndc_y, -1.0)
        
        # Transformar la dirección del rayo del espacio de la cámara al espacio del mundo.
        view = self.get_view_matrix()
        inv_view = glm.inverse(view)
        
        ray_dir_world = glm.normalize(glm.vec3(inv_view * glm.vec4(ray_dir_camera, 0.0)))

        # Crear y devolver el rayo final.
        return Ray(self.position, ray_dir_world)
    
    