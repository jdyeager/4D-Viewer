import pygame
from pygame.locals import QUIT

from geometry.tesseract import make_tesseract
from renderer.window import init_window, clear, swap
from renderer.camera import Camera
from object4d import Object4D


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

    clear()
    camera.apply()
    obj.draw()

    swap()
    clock.tick(60)

  pygame.quit()


if __name__ == '__main__':
  main()
