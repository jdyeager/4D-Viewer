import numpy as np
import pygame

from math4d.rotations import rotation_matrix
from math4d.projections import perspective
from renderer.wireframe import draw_wireframe


# Key bindings: each entry maps a pygame key to (plane, sign).
# sign=+1 means positive rotation in that plane, -1 means negative.
ROTATION_KEYS = {
  # Left hand: 3D rotations (XZ=yaw, YZ=pitch, XY=roll)
  pygame.K_a: ('xz', +1),  # yaw left
  pygame.K_d: ('xz', -1),  # yaw right
  pygame.K_w: ('yz', -1),  # pitch up
  pygame.K_s: ('yz', +1),  # pitch down
  pygame.K_q: ('xy', +1),  # roll counter-clockwise
  pygame.K_e: ('xy', -1),  # roll clockwise
  # Right hand: 4D rotations (ana = -W direction)
  pygame.K_j: ('xw', -1),  # ana -> left
  pygame.K_l: ('xw', +1),  # ana -> right
  pygame.K_i: ('yw', +1),  # ana -> up
  pygame.K_k: ('yw', -1),  # ana -> down
  pygame.K_u: ('zw', +1),  # ana -> front
  pygame.K_o: ('zw', -1),  # ana -> back
}

ROTATION_SPEED = 0.02  # radians per frame


class Object4D:
  """A 4D shape with rotation state and the ability to draw itself.

  Wraps a Shape4D and manages the accumulated 4D rotation matrix.
  Handles keyboard input for rotation and reset, and knows how to
  project and render itself.

  Attributes:
    shape: the underlying Shape4D geometry
    rotation: (4, 4) accumulated rotation matrix
    camera_distance: distance for 4D perspective projection
  """

  def __init__(self, shape, camera_distance=3.0):
    self.shape = shape
    self.rotation = np.eye(4)
    self.camera_distance = camera_distance

  def update(self, keys):
    """Check rotation keys and update rotation state. Called once per frame.

    Handles:
      - Rotation key pairs: accumulate rotation in the corresponding plane
      - X key: reset rotation to identity
    """
    if keys[pygame.K_x]:
      self.rotation = np.eye(4)
    for key, (plane, sign) in ROTATION_KEYS.items():
      if keys[key]:
        self.rotation = self.rotation @ rotation_matrix(plane, sign * ROTATION_SPEED)

  def draw(self):
    """Project to 3D and render as wireframe."""
    rotated = self.shape.vertices @ self.rotation
    verts_3d = perspective(rotated, self.camera_distance)
    draw_wireframe(verts_3d, self.shape.edges)
