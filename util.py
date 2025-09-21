import threading

import cv2
import matplotlib.colors
import numpy as np
import pygame

class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args, **kwargs):
        threading.Thread.join(self, *args, **kwargs)
        return self._return

def generate_rainbow(dimensions : tuple):
    surface = pygame.Surface(dimensions)
    array = pygame.surfarray.pixels3d(surface)
    for i in range(dimensions[1]):
        hue = i / dimensions[1]
        array[:, i, :] = matplotlib.colors.hsv_to_rgb((hue, 1, 1)) * 255
    return surface

def blur(surface, ksize, scale=1):
    if scale > 1:
        scaled = pygame.transform.scale_by(surface, 1/scale)
        array = pygame.surfarray.pixels3d(scaled)
    else:
        array = pygame.surfarray.pixels3d(surface)
    edited = cv2.boxFilter(array, -1, (ksize, ksize))
    del array
    if scale > 1:
        pygame.surfarray.blit_array(scaled, np.array(edited))
        pygame.transform.scale_by(scaled, scale, surface)
    else:
        pygame.surfarray.blit_array(surface, np.array(edited))