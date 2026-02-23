import numpy as np


class Shape4D:
  """Base class for 4D geometric objects.

  Attributes:
    vertices: (N, 4) array of 4D vertex positions [x, y, z, w].
    edges: (M, 2) array of vertex index pairs defining edges.
    faces: list of arrays, each containing vertex indices for one face.
  """

  def __init__(self, vertices, edges, faces=None):
    self.vertices = np.asarray(vertices, dtype=np.float64)
    self.edges = np.asarray(edges, dtype=np.int32)
    self.faces = faces if faces is not None else []

    assert self.vertices.ndim == 2 and self.vertices.shape[1] == 4, \
      f"vertices must be (N, 4), got {self.vertices.shape}"
    assert self.edges.ndim == 2 and self.edges.shape[1] == 2, \
      f"edges must be (M, 2), got {self.edges.shape}"

  @property
  def num_vertices(self):
    return self.vertices.shape[0]

  @property
  def num_edges(self):
    return self.edges.shape[0]

  @property
  def num_faces(self):
    return len(self.faces)
