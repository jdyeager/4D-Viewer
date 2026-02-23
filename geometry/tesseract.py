import numpy as np
from itertools import product
from geometry.base import Shape4D


def make_tesseract():
  """Generate a tesseract (4D hypercube) with vertices at (±1, ±1, ±1, ±1).

  Returns a Shape4D with:
    - 16 vertices (all combinations of ±1 in 4 coordinates)
    - 32 edges (between vertices differing in exactly 1 coordinate)
    - 24 square faces (between vertices differing in exactly 2 coordinates,
      with the other 2 coordinates fixed)
  """
  # 16 vertices: all combinations of -1 and +1 in 4 dimensions
  vertices = np.array(list(product([-1, 1], repeat=4)), dtype=np.float64)

  # 32 edges: connect vertices that differ in exactly 1 coordinate.
  # Two vertices at Hamming distance 1 share an edge.
  edges = []
  for i in range(len(vertices)):
    for j in range(i + 1, len(vertices)):
      diff = np.abs(vertices[i] - vertices[j])
      if np.sum(diff) == 2:  # exactly 1 coord differs by 2 (from -1 to +1)
        edges.append([i, j])
  edges = np.array(edges, dtype=np.int32)

  # 24 square faces: pick 2 axes to vary, fix the other 2.
  # There are C(4,2) = 6 axis pairs, and 2^2 = 4 sign choices for the
  # fixed axes, giving 6 * 4 = 24 faces.
  faces = []
  axes = [0, 1, 2, 3]
  for a in range(4):
    for b in range(a + 1, 4):
      fixed_axes = [x for x in axes if x != a and x != b]
      for sa in [-1, 1]:
        for sb in [-1, 1]:
          # Find the 4 vertices where fixed axes have values sa, sb
          mask = (
            (vertices[:, fixed_axes[0]] == sa) &
            (vertices[:, fixed_axes[1]] == sb)
          )
          face_vert_idxs = np.where(mask)[0]
          # Order them so they form a proper quad (not a bowtie).
          # Sort by angle around the face center.
          center = vertices[face_vert_idxs].mean(axis=0)
          relative = vertices[face_vert_idxs] - center
          angles = np.arctan2(relative[:, b], relative[:, a])
          order = np.argsort(angles)
          faces.append(face_vert_idxs[order])

  return Shape4D(vertices, edges, faces)
