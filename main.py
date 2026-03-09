import pygame
from pygame.locals import QUIT

from geometry.tesseract import make_tesseract
from geometry.pentachoron import make_pentachoron
from geometry.hypersphere import make_hypersphere
from geometry.spherinder import make_spherinder
from renderer.window import init_window, clear, swap
from renderer.camera import Camera
from object4d import Object4D


# Shape catalogue: number keys switch between shapes
SHAPES = {
  pygame.K_1: ('Tesseract', make_tesseract, {}),
  pygame.K_2: ('Pentachoron', make_pentachoron, {"radius": 2.25}),
  pygame.K_3: ('Hypersphere', make_hypersphere,
               {"radius": 2, "n1":6, "n2":8, "n3":10, "interpolation": 1/3}),
  pygame.K_4: ('Spherinder', make_spherinder,
               {"radius": 1.5, "n_lat" : 10, "n_lon": 12, "interpolation": 1/3, "half_height": 1.0}),
}

def main():
  init_window()

  camera = Camera(distance=3.0, sensitivity=.25, zoom_sensitivity=.25)
  obj = Object4D(make_tesseract(), camera_distance=3.0)
  clock = pygame.time.Clock()

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
      camera.handle_event(event)

    keys = pygame.key.get_pressed()
    camera.update(keys)
    obj.update(keys)

    # Shape switching: number keys swap the geometry, reset rotation
    for key, (name, make_fn, kwargs) in SHAPES.items():
      if keys[key]:
        obj.shape = make_fn(**kwargs)
        obj.reset_rotation()
        camera.reset()

    clear()
    camera.apply()
    obj.draw()

    swap()
    clock.tick(60)

  pygame.quit()


if __name__ == '__main__':
  main()
