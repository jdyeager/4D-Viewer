import numpy as np
from geometry.tesseract import make_tesseract


def test_tesseract_counts():
  """Tesseract should have exactly 16 vertices, 32 edges, 24 faces."""
  t = make_tesseract()
  assert t.num_vertices == 16
  assert t.num_edges == 32
  assert t.num_faces == 24


def test_tesseract_vertices_on_hypercube():
  """Every vertex should have all coordinates equal to ±1."""
  t = make_tesseract()
  assert np.all(np.abs(t.vertices) == 1)


def test_tesseract_edge_lengths():
  """Every edge should have length 2 (from -1 to +1 in one coordinate)."""
  t = make_tesseract()
  for e in t.edges:
    v0, v1 = t.vertices[e[0]], t.vertices[e[1]]
    length = np.linalg.norm(v1 - v0)
    assert np.isclose(length, 2.0), f"Edge length {length}, expected 2.0"


def test_tesseract_edges_differ_in_one_coord():
  """Each edge should connect vertices differing in exactly 1 coordinate."""
  t = make_tesseract()
  for e in t.edges:
    diff = t.vertices[e[0]] != t.vertices[e[1]]
    assert np.sum(diff) == 1


def test_tesseract_faces_are_quads():
  """Every face should have exactly 4 vertices."""
  t = make_tesseract()
  for face in t.faces:
    assert len(face) == 4, f"Face has {len(face)} vertices, expected 4"


def test_tesseract_faces_are_planar_squares():
  """Each face should be a square: 4 coplanar vertices with equal side lengths."""
  t = make_tesseract()
  for face in t.faces:
    verts = t.vertices[face]
    # Check all 4 side lengths (consecutive pairs in winding order)
    side_lengths = []
    for k in range(4):
      side = np.linalg.norm(verts[(k + 1) % 4] - verts[k])
      side_lengths.append(side)
    # All sides should be equal (it's a square)
    assert all(np.isclose(s, side_lengths[0]) for s in side_lengths), \
      f"Side lengths not equal: {side_lengths}"
    # Side length should be 2
    assert np.isclose(side_lengths[0], 2.0)


def test_tesseract_no_duplicate_edges():
  """No edge should appear twice."""
  t = make_tesseract()
  edge_set = set()
  for e in t.edges:
    key = (min(e[0], e[1]), max(e[0], e[1]))
    assert key not in edge_set, f"Duplicate edge: {key}"
    edge_set.add(key)


def test_tesseract_no_duplicate_faces():
  """No face should appear twice (same set of vertex indices)."""
  t = make_tesseract()
  face_set = set()
  for face in t.faces:
    key = frozenset(face)
    assert key not in face_set, f"Duplicate face: {key}"
    face_set.add(key)
