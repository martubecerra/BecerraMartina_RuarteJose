# src/model.py

class Vertex:
    """Representa un único atributo de vértice (ej: posiciones)."""
    def __init__(self, name, format, array):
        self.__name = name
        self.__format = format
        self.__array = array

    @property
    def name(self):
        return self.__name

    @property
    def format(self):
        return self.__format

    @property
    def array(self):
        return self.__array

class VertexLayout:
    """Agrupa un conjunto de atributos de vértice para describir un modelo."""
    def __init__(self):
        self.__attributes = []

    def add_attribute(self, name: str, format: str, array):
        self.__attributes.append(Vertex(name, format, array))

    def get_attributes(self):
        return self.__attributes

class Model:
    """Clase base para todos los modelos 3D del proyecto."""
    def __init__(self, vertices=None, indices=None, colors=None, normals=None, texcoords=None):
        self.indices = indices
        self.vertex_layout = VertexLayout()
        
        if vertices is not None:
            self.vertex_layout.add_attribute("in_pos", "3f", vertices)
        if colors is not None:
            self.vertex_layout.add_attribute("in_color", "3f", colors)
        if normals is not None:
            self.vertex_layout.add_attribute("in_normal", "3f", normals)
        if texcoords is not None:
            self.vertex_layout.add_attribute("in_uv", "2f", texcoords)