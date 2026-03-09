import numpy as np
from geometry.base import Shape3D


def make_sphere(radius=1.0, n_lat=10, n_lon=12, interpolation=0):
  """Generate a tessellated 2-sphere using spherical coordinates.

  Parameterized by two angles:
    theta in [0, pi]     — latitude (pole to pole)
    phi   in [0, 2*pi)   — longitude (wraps around)

  Coordinates:
    x = R * sin(theta) * cos(phi)
    y = R * sin(theta) * sin(phi)
    z = R * cos(theta)

  Args:
    radius: radius of the sphere
    n_lat: number of latitude steps (pole to pole)
    n_lon: number of longitude steps (around the equator)
    interpolation: [0,1], 0 for angle interpolation, 1 for axis distance interpolation

  Returns a Shape3D with vertices on S² and edges connecting adjacent
  grid points.
  """
  theta_vals_angle = np.linspace(0, np.pi, n_lat + 1)
  theta_vals_dist = np.arccos(np.linspace(1, -1, n_lat + 1))
  theta_vals = (1 - interpolation) * theta_vals_angle + interpolation * theta_vals_dist
  phi_vals = np.linspace(0, 2 * np.pi, n_lon, endpoint=False)

  vertices = []
  idx = {}

  for i, theta in enumerate(theta_vals):
    for j, phi in enumerate(phi_vals):
      x = radius * np.sin(theta) * np.cos(phi)
      y = radius * np.sin(theta) * np.sin(phi)
      z = radius * np.cos(theta)
      idx[(i, j)] = len(vertices)
      vertices.append([x, y, z])

  vertices = np.array(vertices, dtype=np.float64)

  edge_set = set()

  def add_edge(a, b):
    if a != b:  # skip degenerate edges at poles
      edge_set.add((min(a, b), max(a, b)))

  for i in range(len(theta_vals)):
    for j in range(len(phi_vals)):
      v = idx[(i, j)]
      # Edge along theta (toward next latitude ring)
      if i + 1 < len(theta_vals):
        add_edge(v, idx[(i + 1, j)])
      # Edge along phi (wraps around)
      j_next = (j + 1) % len(phi_vals)
      add_edge(v, idx[(i, j_next)])

  edges = np.array(sorted(edge_set), dtype=np.int32)

  return Shape3D(vertices, edges)
