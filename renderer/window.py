import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (
  glClearColor, glEnable, glLineWidth, glClear, glMatrixMode, glViewport,
  GL_DEPTH_TEST, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
  GL_PROJECTION, GL_MODELVIEW,
  GL_LINE_SMOOTH, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
  glBlendFunc, glHint, GL_LINE_SMOOTH_HINT, GL_NICEST,
  glGetIntegerv, GL_VIEWPORT
)
from OpenGL.GLU import gluPerspective
import ctypes


def init_window(width=800, height=600, title="4D Viewer"):
  """Create a Pygame window with an OpenGL rendering context.

  Sets up:
    - A window of the given size with OpenGL + double buffering
    - Dark background (near-black)
    - Depth testing enabled (so closer geometry occludes farther)
    - A perspective projection for the 3D→2D step (OpenGL handles this)

  Args:
    width: window width in pixels
    height: window height in pixels
    title: window title

  Returns:
    The Pygame display surface (mostly unused directly — we draw via OpenGL)
  """
  pygame.init()

  # On macOS Retina displays, the window's "point" size differs from its
  # actual pixel size. We need to query the real framebuffer size and tell
  # OpenGL to render at full resolution, otherwise it renders at half res
  # and upscales (blurry/blocky).
  surface = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
  pygame.display.set_caption(title)

  # On Retina, pygame may report the point size here. The actual framebuffer
  # can be queried via OpenGL after context creation.
  viewport = (ctypes.c_int * 4)()
  glGetIntegerv(GL_VIEWPORT, viewport)
  fb_width, fb_height = viewport[2], viewport[3]
  glViewport(0, 0, fb_width, fb_height)

  # Dark background
  glClearColor(0.05, 0.05, 0.08, 1.0)

  # Depth testing: fragments closer to the camera overwrite farther ones
  glEnable(GL_DEPTH_TEST)

  # Anti-aliased lines: smooths the staircase effect on diagonal/curved edges
  glEnable(GL_LINE_SMOOTH)
  glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
  glEnable(GL_BLEND)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

  # Thicker lines so the wireframe is easy to see
  glLineWidth(2.0)

  # Set up a perspective projection matrix on the PROJECTION matrix.
  # This controls how 3D coordinates map to 2D screen pixels.
  # We set it here once; the camera operates on the separate MODELVIEW
  # matrix, so resetting modelview each frame won't affect this.
  #   fov=45°: field of view (how wide the camera lens is)
  #   aspect: width/height so circles look circular, not elliptical
  #   near=0.1, far=50: clipping planes — anything closer than 0.1 or
  #     farther than 50 units from the camera is not drawn
  glMatrixMode(GL_PROJECTION)
  gluPerspective(45, fb_width / fb_height, 0.1, 50.0)

  # Switch back to modelview for all subsequent operations (camera, etc.)
  glMatrixMode(GL_MODELVIEW)

  return surface


def clear():
  """Clear the screen for a new frame."""
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def swap():
  """Swap the front and back buffers to display the rendered frame.

  We use double buffering: draw to an invisible back buffer, then swap
  it to the screen all at once. This prevents flickering.
  """
  pygame.display.flip()
