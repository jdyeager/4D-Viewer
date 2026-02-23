import numpy as np


def rotation_matrix(plane, angle):
  """Build a 4x4 rotation matrix for rotation in the given plane.

  A rotation in 4D acts on a 2D plane spanned by two coordinate axes,
  leaving the other two axes unchanged. This is analogous to how a 3D
  rotation acts on a plane (e.g., XY) and leaves the third axis (Z) fixed.

  Args:
    plane: two axis letters, e.g. 'xy', 'xz', 'yz', 'xw', 'yw', 'zw'.
           Order matters: 'yx' rotates in the opposite direction to 'xy'.
    angle: rotation angle in radians

  Returns:
    (4, 4) rotation matrix
  """
  # Map axis letters to indices: x=0, y=1, z=2, w=3
  axis_index = {'x': 0, 'y': 1, 'z': 2, 'w': 3}

  plane = plane.lower()
  assert len(plane) == 2 and plane[0] in axis_index and plane[1] in axis_index \
    and plane[0] != plane[1], \
    f"plane must be two distinct axis letters like 'xy', got '{plane}'"

  i = axis_index[plane[0]]
  j = axis_index[plane[1]]

  c = np.cos(angle)
  s = np.sin(angle)

  # Start with identity, then fill in the 2x2 rotation block
  # at rows/cols (i, j). For row-vector convention (v @ M):
  #   axis i:  cos θ, sin θ
  #   axis j: -sin θ, cos θ
  # All other diagonal entries remain 1.
  m = np.eye(4, dtype=np.float64)
  m[i, i] = c
  m[i, j] = s
  m[j, i] = -s
  m[j, j] = c

  return m


def compose(*matrices):
  """Compose multiple 4x4 transformation matrices left-to-right.

  compose(A, B, C) returns A @ B @ C. With row-vector convention
  (v @ M), this applies A first, then B, then C.
  """
  result = np.eye(4, dtype=np.float64)
  for m in matrices:
    result = result @ m
  return result
