import numpy as np
from math4d.rotations import rotation_matrix, compose


def test_rotation_is_orthogonal():
  """Every rotation matrix should satisfy M @ M^T = I."""
  for plane in ['xy', 'xz', 'xw', 'yz', 'yw', 'zw']:
    for angle in [0, 0.5, np.pi / 4, np.pi / 2, np.pi, -1.3]:
      m = rotation_matrix(plane, angle)
      product = m @ m.T
      assert np.allclose(product, np.eye(4)), \
        f"Not orthogonal for plane={plane}, angle={angle}"


def test_rotation_determinant_is_one():
  """Rotation matrices should have determinant +1 (proper rotation)."""
  for plane in ['xy', 'xz', 'xw', 'yz', 'yw', 'zw']:
    m = rotation_matrix(plane, 0.7)
    assert np.isclose(np.linalg.det(m), 1.0), \
      f"det={np.linalg.det(m)} for plane={plane}"


def test_zero_angle_is_identity():
  """Rotation by 0 should give the identity matrix."""
  for plane in ['xy', 'xz', 'xw', 'yz', 'yw', 'zw']:
    m = rotation_matrix(plane, 0.0)
    assert np.allclose(m, np.eye(4))


def test_rotation_leaves_other_axes_fixed():
  """Rotation in the XY plane should not affect Z or W components."""
  m = rotation_matrix('xy', np.pi / 3)
  # A vector purely along Z should be unchanged
  v_z = np.array([0, 0, 1, 0])
  assert np.allclose(v_z @ m, v_z)
  # A vector purely along W should be unchanged
  v_w = np.array([0, 0, 0, 1])
  assert np.allclose(v_w @ m, v_w)


def test_90_degree_rotation():
  """Rotating (1,0,0,0) by 90° in XY should give (0,1,0,0)."""
  m = rotation_matrix('xy', np.pi / 2)
  v = np.array([1, 0, 0, 0])
  result = v @ m
  expected = np.array([0, 1, 0, 0])
  assert np.allclose(result, expected), f"Got {result}, expected {expected}"


def test_reverse_plane_reverses_direction():
  """'yx' should rotate in the opposite direction to 'xy'."""
  angle = 0.7
  m_xy = rotation_matrix('xy', angle)
  m_yx = rotation_matrix('yx', angle)
  # They should be transposes of each other (inverse rotations)
  assert np.allclose(m_xy, m_yx.T)


def test_compose_identity():
  """Composing with identity should change nothing."""
  m = rotation_matrix('xw', 1.2)
  result = compose(np.eye(4), m)
  assert np.allclose(result, m)
  result = compose(m, np.eye(4))
  assert np.allclose(result, m)


def test_compose_inverse():
  """Composing a rotation with its inverse (negative angle) should give identity."""
  m = rotation_matrix('zw', 0.8)
  m_inv = rotation_matrix('zw', -0.8)
  result = compose(m, m_inv)
  assert np.allclose(result, np.eye(4))


def test_compose_order():
  """compose(A, B) should equal A @ B."""
  a = rotation_matrix('xy', 0.5)
  b = rotation_matrix('zw', 0.3)
  assert np.allclose(compose(a, b), a @ b)


def test_compose_three():
  """compose(A, B, C) should equal A @ B @ C."""
  a = rotation_matrix('xy', 0.5)
  b = rotation_matrix('zw', 0.3)
  c = rotation_matrix('xw', -0.9)
  assert np.allclose(compose(a, b, c), a @ b @ c)


def test_compose_three_not_commutative():
  """Rotations in different planes generally don't commute.

  compose(A, B, C) should differ from compose(C, B, A) when the
  rotations share an axis (e.g., XY and XW both involve X).
  """
  a = rotation_matrix('xy', 0.5)
  b = rotation_matrix('xw', 0.3)
  c = rotation_matrix('yw', 0.7)
  forward = compose(a, b, c)
  backward = compose(c, b, a)
  assert not np.allclose(forward, backward)


def test_rotation_on_tesseract_vertex():
  """180° rotation in XW should send (1,1,1,1) to (-1,1,1,-1)."""
  m = rotation_matrix('xw', np.pi)
  v = np.array([1, 1, 1, 1])
  result = v @ m
  expected = np.array([-1, 1, 1, -1])
  assert np.allclose(result, expected), f"Got {result}, expected {expected}"
