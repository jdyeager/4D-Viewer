import numpy as np
from math4d.projections import orthographic, perspective
from geometry.tesseract import make_tesseract


def test_orthographic_shape():
  """Output should be (N, 3) when input is (N, 4)."""
  verts = np.ones((10, 4))
  result = orthographic(verts)
  assert result.shape == (10, 3)


def test_orthographic_drops_w():
  """Orthographic projection should return the XYZ components unchanged."""
  verts = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
  ], dtype=np.float64)
  result = orthographic(verts)
  expected = np.array([[1, 2, 3], [5, 6, 7]])
  assert np.allclose(result, expected)


def test_perspective_shape():
  """Output should be (N, 3) when input is (N, 4)."""
  verts = np.ones((10, 4))
  result = perspective(verts, camera_distance=5.0)
  assert result.shape == (10, 3)


def test_perspective_at_w_zero():
  """Vertices at w=0 should be scaled by 1/camera_distance."""
  verts = np.array([[3, 6, 9, 0]], dtype=np.float64)
  result = perspective(verts, camera_distance=3.0)
  expected = np.array([[1, 2, 3]])
  assert np.allclose(result, expected)


def test_perspective_positive_w_enlarges():
  """Vertices with positive w (closer to 4D camera) should appear larger."""
  v_near = np.array([[1, 0, 0, 1]], dtype=np.float64)  # w = +1
  v_far = np.array([[1, 0, 0, -1]], dtype=np.float64)  # w = -1
  d = 3.0
  near_proj = perspective(v_near, d)
  far_proj = perspective(v_far, d)
  # near should have larger x than far (both started at x=1)
  assert near_proj[0, 0] > far_proj[0, 0]


def test_perspective_tesseract_inner_outer():
  """Perspective projection of a tesseract should produce two nested cubes.

  Vertices at w=+1 project to a larger cube, vertices at w=-1 to a smaller
  cube, creating the classic "cube within a cube" appearance.
  """
  t = make_tesseract()
  proj = perspective(t.vertices, camera_distance=3.0)

  # Split into w=+1 and w=-1 groups
  w_pos = t.vertices[:, 3] > 0
  w_neg = t.vertices[:, 3] < 0

  # The w=+1 vertices should project further from origin (larger cube)
  avg_dist_pos = np.mean(np.linalg.norm(proj[w_pos], axis=1))
  avg_dist_neg = np.mean(np.linalg.norm(proj[w_neg], axis=1))
  assert avg_dist_pos > avg_dist_neg


def test_perspective_large_distance_approaches_orthographic():
  """With a very large camera distance, perspective ≈ orthographic (scaled)."""
  t = make_tesseract()
  d = 1000.0
  persp = perspective(t.vertices, camera_distance=d)
  ortho = orthographic(t.vertices)
  # perspective should be approximately ortho / d (since scale ≈ d for all)
  assert np.allclose(persp, ortho / d, atol=1e-3)