from OpenGL.GL import glBegin, glEnd, glVertex3fv, glColor3f, GL_LINES


def draw_wireframe(vertices_3d, edges, color=(0.4, 0.8, 1.0)):
  """Draw a wireframe from projected 3D vertices and edge index pairs.

  This is the simplest possible rendering: one color, straight lines
  between vertex pairs. OpenGL's pipeline handles the 3D→2D perspective
  projection (set up in window.py) and rasterizes the lines to pixels.

  Args:
    vertices_3d: (N, 3) array of 3D positions (already projected from 4D)
    edges: (M, 2) array of vertex index pairs
    color: RGB tuple, each component in [0, 1]
  """
  glColor3f(*color)
  glBegin(GL_LINES)
  for e in edges:
    glVertex3fv(vertices_3d[e[0]])
    glVertex3fv(vertices_3d[e[1]])
  glEnd()
