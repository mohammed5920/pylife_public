import pygame
import numpy as np

import util
import engine

pygame.init()
SCALE = 1
RESOLUTION = np.subtract(pygame.display.get_desktop_sizes()[0], (100,100))
screen = pygame.display.set_mode(RESOLUTION, pygame.SCALED)
pygame.event.set_blocked(None)
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.VIDEORESIZE])

FPS = pygame.display.get_current_refresh_rate()
clock = pygame.time.Clock()
current_array = np.zeros((RESOLUTION[0], RESOLUTION[1], 3), np.uint8)

rainbow = util.generate_rainbow(current_array.shape[:2])
rainbow_y = 0
buffer = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))
buffer.set_colorkey((255,255,255))
blur_buffer = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))
blur_buffer.set_alpha(128)

clicked = simulating = False
mouse_size = pretty = 1
engine.iterate_game(current_array)

def render(current_array, pretty_render=False, rainbow_offset=0):
    if pretty_render:
        screen.blit(rainbow, (0, rainbow_offset % RESOLUTION[1]))
        if rainbow_offset % RESOLUTION[1]:
            screen.blit(rainbow, (0, rainbow_offset % RESOLUTION[1] - RESOLUTION[1]))
        pygame.surfarray.blit_array(buffer, current_array)
        screen.blit(buffer, (0,0))
        blur_buffer.blit(screen, (0,0)) #copy that
        util.blur(blur_buffer, 16, max(4//SCALE, 1)) #and blur it
        screen.blit(blur_buffer, (0,0)) #blit that back on the screen
    else:
        pygame.surfarray.blit_array(screen, current_array)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 3): #right/left click
                clicked = event.button
            if event.button == 4 and mouse_size*2 < min(RESOLUTION):
                mouse_size *= 2
            if event.button == 5 and mouse_size > 1:
                mouse_size //= 2
        if event.type == pygame.MOUSEBUTTONUP and event.button in (1,3): 
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulating = not simulating
            if event.key == pygame.K_BACKSPACE:
                current_array = np.zeros((RESOLUTION[0], RESOLUTION[1], 3), np.uint8)
                simulating = False
            if event.key == pygame.K_e and not simulating:
                current_array = engine.iterate_game(current_array)
            if event.key == pygame.K_p:
                pretty = not pretty
    
    mouse_pos = pygame.mouse.get_pos()
    if mouse_size > 1:
        mouse_pos = (int(mouse_pos[0] - mouse_size*0.5), #centering
                     int(mouse_pos[1] - mouse_size*0.5)) 
    if clicked:
        current_array[max(mouse_pos[0], 0) : mouse_pos[0] + mouse_size, 
                      max(mouse_pos[1], 0) : mouse_pos[1] + mouse_size] = (clicked == 1)*255
    
    if not simulating:
        render(current_array)
        mouse_hover = pygame.Surface((mouse_size, mouse_size))
        mouse_hover.fill((255, 255, 255))
        mouse_hover.set_alpha(64)
        screen.blit(mouse_hover, mouse_pos)
    else: 
        iterate_thread = util.ThreadWithReturnValue(target=engine.iterate_game, args=[current_array])
        iterate_thread.start()
        render(current_array, pretty_render=pretty, rainbow_offset=rainbow_y)
        if pretty: rainbow_y+=1
        current_array = iterate_thread.join()
        
    pygame.display.flip()  
    clock.tick(FPS) 