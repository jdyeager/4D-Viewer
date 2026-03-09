import numpy as np
from geometry.base import Shape4D


def make_hypersphere(radius=1.5, n1=6, n2=8, n3=12, interpolation=0):
  """Generate a tessellated 3-sphere (hypersphere) using hyperspherical coords.

  The 3-sphere S³ is parameterized by three angles:
    phi1 in [0, pi]    — "4D latitude" (pole to pole along W axis)
    phi2 in [0, pi]    — second latitude
    phi3 in [0, 2*pi]  — longitude (wraps around)

  Coordinates:
    x = R * sin(phi1) * sin(phi2) * cos(phi3)
    y = R * sin(phi1) * sin(phi2) * sin(phi3)
    z = R * sin(phi1) * cos(phi2)
    w = R * cos(phi1)

  The grid has poles at phi1=0 (w=+R) and phi1=pi (w=-R), where
  all phi2/phi3 values collapse to a single point. Like a UV sphere
  in 3D, the mesh is denser near the poles. This is a known tradeoff
  for simplicity; more uniform alternatives (Hopf fibration, recursive
  subdivision of a 600-cell) are significantly more complex.

  Args:
    radius: radius of the hypersphere
    n1: number of steps along phi1 (pole-to-pole, higher = more rings)
    n2: number of steps along phi2 (higher = more latitude lines)
    n3: number of steps along phi3 (longitude, higher = more meridians)
    interpolation: [0,1], 0 for angle interpolation, 1 for axis distance interpolation

  Returns a Shape4D with vertices on S³ and edges connecting adjacent
  grid points.
  """
  # Sample the angles. phi1 and phi2 include both endpoints (0 and pi).
  phi1_vals_angle = np.linspace(0, np.pi, n1 + 1)
  phi2_vals_angle = np.linspace(0, np.pi, n2 + 1)
  # Equidistant along their axis
  phi1_vals_dist = np.arccos(np.linspace(1, -1, n1 + 1))
  phi2_vals_dist = np.arccos(np.linspace(1, -1, n2 + 1))
  # A little mixing of the two
  phi1_vals = (1 - interpolation) * phi1_vals_angle + interpolation * phi1_vals_dist
  phi2_vals = (1 - interpolation) * phi2_vals_angle + interpolation * phi2_vals_dist
  # phi3 wraps around, so we exclude the endpoint (0 ≈ 2*pi).
  phi3_vals = np.linspace(0, 2 * np.pi, n3, endpoint=False)

  # Generate all vertices on the grid
  vertices = []
  # Map (i, j, k) grid indices to vertex index in the flat list
  idx = {}

  for i, p1 in enumerate(phi1_vals):
    for j, p2 in enumerate(phi2_vals):
      for k, p3 in enumerate(phi3_vals):
        x = radius * np.sin(p1) * np.sin(p2) * np.cos(p3)
        y = radius * np.sin(p1) * np.sin(p2) * np.sin(p3)
        z = radius * np.sin(p1) * np.cos(p2)
        w = radius * np.cos(p1)
        idx[(i, j, k)] = len(vertices)
        vertices.append([x, y, z, w])

  vertices = np.array(vertices, dtype=np.float64)

  # Generate edges between adjacent grid points
  edge_set = set()

  def add_edge(a, b):
    if a != b:  # skip degenerate edges at poles
      edge_set.add((min(a, b), max(a, b)))

  for i in range(len(phi1_vals)):
    for j in range(len(phi2_vals)):
      for k in range(len(phi3_vals)):
        v = idx[(i, j, k)]
        # Edge along phi1 (toward next ring)
        if i + 1 < len(phi1_vals):
          add_edge(v, idx[(i + 1, j, k)])
        # Edge along phi2
        if j + 1 < len(phi2_vals):
          add_edge(v, idx[(i, j + 1, k)])
        # Edge along phi3 (wraps around)
        k_next = (k + 1) % len(phi3_vals)
        add_edge(v, idx[(i, j, k_next)])

  edges = np.array(sorted(edge_set), dtype=np.int32)

  return Shape4D(vertices, edges)
