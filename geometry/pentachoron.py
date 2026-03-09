import numpy as np
from itertools import combinations
from geometry.base import Shape4D


def make_pentachoron(radius = 2):
  """Generate a pentachoron (5-cell / 4D simplex).

  The pentachoron is the 4D analogue of the tetrahedron. It has:
    - 5 vertices, all equidistant from each other
    - 10 edges (every pair of vertices is connected)
    - 10 triangular faces (every triple of vertices forms a face)

  The vertices are constructed by embedding a regular tetrahedron in
  the w=0 hyperplane, then adding a 5th vertex along the +w axis at
  the correct distance to make all edges equal. The result is then
  centered at the origin so rotations behave symmetrically.

  Returns a Shape4D with 5 vertices, 10 edges, 10 triangular faces.
  """
  # A regular tetrahedron with edge length 2, centered at the origin in XYZ:
  #   vertex 0: ( 1,  1,  1, 0)
  #   vertex 1: ( 1, -1, -1, 0)
  #   vertex 2: (-1,  1, -1, 0)
  #   vertex 3: (-1, -1,  1, 0)
  # These all have distance 2√2 from each other — we'll normalize later.
  tet = np.array([
    [ 1,  1,  1, 0],
    [ 1, -1, -1, 0],
    [-1,  1, -1, 0],
    [-1, -1,  1, 0],
  ], dtype=np.float64)

  # The center of these 4 vertices (in 4D):
  # center_tet = tet.mean(axis=0)  # should be (0, 0, 0, 0)

  # Edge length of this tetrahedron:
  edge_len = np.linalg.norm(tet[0] - tet[1])  # 2√2

  # The 5th vertex sits along the +w axis, at the same distance from each
  # of the 4 tetrahedron vertices. By symmetry, its xyz coordinates equal
  # the tetrahedron center's xyz (which is 0,0,0).
  # Solve: |v5 - v0| = edge_len, where v5 = (0, 0, 0, w5) and v0 = (1, 1, 1, 0)
  #   sqrt(1 + 1 + 1 + w5^2) = 2√2
  #   3 + w5^2 = 8
  #   w5 = √5
  w5 = np.sqrt(edge_len**2 - np.sum(tet[0, :3]**2))
  v5 = np.array([0, 0, 0, w5])

  vertices = np.vstack([tet, [v5]])

  # Center at the origin so rotations are symmetric
  vertices -= vertices.mean(axis=0)

  # Normalize so the vertices sit on the unit hypersphere (radius 1).
  # This makes it a similar size to the tesseract for viewing.
  max_dist = np.max(np.linalg.norm(vertices, axis=1))
  vertices /= max_dist
  vertices *= radius

  # 10 edges: every pair of 5 vertices
  edges = np.array(list(combinations(range(5), 2)), dtype=np.int32)

  # 10 faces: every triple of 5 vertices
  faces = [np.array(f) for f in combinations(range(5), 3)]

  return Shape4D(vertices, edges, faces)
