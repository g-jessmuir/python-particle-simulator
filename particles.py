import pyglet
import random
import math
from pyglet.window import mouse
particle_number = 10000
window_size = 800
window = pyglet.window.Window(window_size, window_size)
mouse_pressed = False
mouse_coords = [0, 0]

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        global mouse_pressed
        mouse_pressed = True
        global mouse_coords
        mouse_coords = [x, y]
    elif button == mouse.RIGHT:
        window.clear()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global mouse_coords
    mouse_coords = [x, y]

@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == mouse.LEFT:
        global mouse_pressed
        mouse_pressed = False

#fps display bit
fps_display = pyglet.clock.ClockDisplay()
@window.event
def on_draw():
    fps_display.draw()

class Particle:
    def __init__(self, xpos, ypos):
        self.pos = [xpos, ypos]
        self.velocity = [0, 0]

#initialization
particles = [Particle(random.randint(0, window_size), random.randint(0, window_size)) for i in range(particle_number)]
particle_coords = []
particle_colours = []
for i in range(len(particles)):
    particle_coords.append(particles[i].pos[0])
    particle_coords.append(particles[i].pos[1])
for j in range(len(particles)):
    for i in range(3):
        particle_colours.append(random.randint(128, 255))

def update_physics():
    mc = mouse_coords
    global particle_coords
    particle_coords = []
    
    def new_pos(particle):
        vector = [mc[0] - particle.pos[0], mc[1] - particle.pos[1]]
        magnitude = math.sqrt(vector[0]**2 + vector[1]**2) + 0.000001
        unit_vector = [vector[0] / magnitude, vector[1] / magnitude]
        particle.velocity = [particle.velocity[0] + unit_vector[0], particle.velocity[1] + unit_vector[1]]
        particle.pos = [particle.pos[0] + particle.velocity[0], particle.pos[1] + particle.velocity[1]]
    
    for particle in particles:
        if(mouse_pressed):
            new_pos(particle)
            
        else:
            particle.velocity = [0, 0]
        particle_coords.append(round(particle.pos[0]))
        particle_coords.append(round(particle.pos[1]))

def tick(dt):
    update_physics()
    window.clear()
    pyglet.graphics.draw(particle_number, pyglet.gl.GL_POINTS, 
        ('v2i', particle_coords),
        ('c3B', particle_colours)
    )

pyglet.clock.schedule_interval(tick, 1/60)
pyglet.app.run()
