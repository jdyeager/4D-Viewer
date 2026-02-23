from OpenGL.GL import (
  glLoadIdentity, glTranslatef, glRotatef,
  GL_MODELVIEW, glMatrixMode,
)


class Camera:
  """Orbiting 3D camera controlled by mouse drag and scroll wheel.

  The camera conceptually sits on a sphere looking at the origin.
  Mouse dragging rotates the viewing angle (orbiting around the object).
  Scroll wheel changes the distance (zoom).

  Internally this is implemented by rebuilding the OpenGL modelview matrix
  each frame: first translate back by `distance`, then apply X and Y
  rotations. Since OpenGL has no real camera, this moves the world
  in the opposite direction.

  Attributes:
    distance: how far the camera is from the origin (scroll to change)
    rot_x: rotation around the X axis in degrees (vertical mouse drag)
    rot_y: rotation around the Y axis in degrees (horizontal mouse drag)
    sensitivity: how many degrees per pixel of mouse movement
    zoom_sensitivity: how far the camera zooms per scroll event
    zoom_speed: how fast the camera zooms to new target distance
    dragging: flag to track is user is actively dragging mouse
  """

  def __init__(self, distance=5.0, sensitivity=0.5, zoom_sensitivity=0.5, zoom_speed=0.1):
    self.distance = distance
    self.target_distance = distance  # where we're zooming toward
    self.rot_x = 0.0  # degrees
    self.rot_y = 0.0  # degrees
    self.sensitivity = sensitivity
    self.zoom_sensitivity = zoom_sensitivity
    self.zoom_speed = zoom_speed  # lerp factor per frame (0-1, higher = faster)
    self.dragging = False

  def handle_event(self, event):
    """Process a Pygame event. Call this for every event in the event loop.

    Handles:
      - MOUSEBUTTONDOWN (left click): start dragging
      - MOUSEBUTTONUP (left click): stop dragging
      - MOUSEMOTION while dragging: orbit the camera
      - MOUSEWHEEL: zoom in/out
    """
    import pygame

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      self.dragging = True

    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      self.dragging = False

    elif event.type == pygame.MOUSEMOTION and self.dragging:
      dx, dy = event.rel  # pixels moved since last motion event
      self.rot_y += dx * self.sensitivity
      self.rot_x += dy * self.sensitivity

    elif event.type == pygame.MOUSEWHEEL:
      self.target_distance -= event.y * self.zoom_sensitivity
      self.target_distance = max(1.0, self.target_distance)

  def apply(self):
    """Set the OpenGL modelview matrix to reflect current camera state.

    Called once per frame, before drawing. Replaces the current modelview
    matrix entirely (no accumulation across frames). Also smoothly
    interpolates the zoom distance toward its target.
    """
    # Smoothly approach target zoom distance.
    # Each frame we close 'zoom_speed' fraction of the remaining gap.
    # At 0.1, it takes ~20-30 frames to visually settle.
    self.distance += (self.target_distance - self.distance) * self.zoom_speed

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Order matters: OpenGL applies transforms in reverse order of calls.
    # We want: first rotate the world, then push it back from the camera.
    # So we call translate first, then rotate.
    glTranslatef(0, 0, -self.distance)
    glRotatef(self.rot_x, 1, 0, 0)  # rotate around world X axis
    glRotatef(self.rot_y, 0, 1, 0)  # rotate around world Y axis
