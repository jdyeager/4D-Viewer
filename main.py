import numpy as np
import pygame
from pygame.locals import QUIT

from geometry.tesseract import make_tesseract
from math4d.rotations import rotation_matrix
from math4d.projections import perspective
from renderer.window import init_window, clear, swap
from renderer.wireframe import draw_wireframe
from renderer.camera import Camera


# Key bindings: each entry maps a pygame key to (plane, sign).
# sign=+1 means positive rotation in that plane, -1 means negative.
KEY_BINDINGS = {
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


def main():
  init_window()

  camera = Camera(distance=3.0, sensitivity=.25, zoom_sensitivity=.25)
  tesseract = make_tesseract()
  clock = pygame.time.Clock()

  # Accumulated 4D rotation matrix, updated each frame
  rotation = np.eye(4)

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
      camera.handle_event(event)

    # Check which rotation keys are currently held down
    keys = pygame.key.get_pressed()
    for key, (plane, sign) in KEY_BINDINGS.items():
      if keys[key]:
        rotation = rotation @ rotation_matrix(plane, sign * ROTATION_SPEED)
    if keys[pygame.K_x]:
      rotation = np.eye(4)
    if keys[pygame.K_z]:
      camera.rot_x = 0.0
      camera.rot_y = 0.0

    clear()
    camera.apply()

    # Apply 4D rotation, then project 4D → 3D
    rotated = tesseract.vertices @ rotation
    verts_3d = perspective(rotated, camera_distance=3.0)
    draw_wireframe(verts_3d, tesseract.edges)

    swap()
    clock.tick(60)

  pygame.quit()


if __name__ == '__main__':
  main()
