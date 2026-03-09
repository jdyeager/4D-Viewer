import numpy as np
from geometry.base import Shape4D


def make_prism(shape3d, half_height=0.5):
  """Extrude a 3D shape along the W axis to produce a 4D prism.

  Creates two copies of the 3D shape: one at w = -half_height ("bottom")
  and one at w = +half_height ("top"). Connects corresponding vertices
  between the two copies with vertical edges along W.

  The resulting Shape4D has:
    - 2N vertices (N from bottom + N from top)
    - 2M + N edges (M edges duplicated on both caps + N vertical edges)
    - Original faces duplicated on both caps, plus rectangular side faces
      connecting each original edge to its copy

  Args:
    shape3d: a Shape3D to extrude
    half_height: half the extent along the W axis

  Returns a Shape4D.
  """
  n = shape3d.num_vertices

  # Bottom copy: original xyz at w = -half_height
  # Top copy: original xyz at w = +half_height
  w_bottom = np.full((n, 1), -half_height)
  w_top = np.full((n, 1), half_height)
  verts_bottom = np.hstack([shape3d.vertices, w_bottom])
  verts_top = np.hstack([shape3d.vertices, w_top])
  vertices = np.vstack([verts_bottom, verts_top])

  # Edges: bottom copy edges, top copy edges (indices shifted by n),
  # and vertical edges connecting each vertex to its counterpart.
  edges_bottom = shape3d.edges
  edges_top = shape3d.edges + n
  edges_vertical = np.column_stack([np.arange(n), np.arange(n) + n])
  edges = np.vstack([edges_bottom, edges_top, edges_vertical])

  # Faces: bottom and top cap faces, plus side quads.
  faces = []

  # Bottom cap faces (same indices)
  for face in shape3d.faces:
    faces.append(np.array(face))

  # Top cap faces (shifted by n)
  for face in shape3d.faces:
    faces.append(np.array(face) + n)

  # Side faces: for each original edge (a, b), the side quad is
  # (a, b, b+n, a+n) — a rectangle connecting bottom edge to top edge.
  for e in shape3d.edges:
    a, b = e[0], e[1]
    faces.append(np.array([a, b, b + n, a + n]))

  return Shape4D(vertices, edges, faces)
