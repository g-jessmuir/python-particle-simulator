import pyglet
import random
import math
from pyglet.window import mouse
particle_number = 4
window_size = 600
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
'''
#fps display bit
fps_display = pyglet.clock.ClockDisplay()
@window.event
def on_draw():
    fps_display.draw()'''

class Particle:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.velocity = [5, -5]

    def apply_force(self, applied_force):
        self.velocity[0] += applied_force[0]
        self.velocity[1] += applied_force[1]
        self.xpos += self.velocity[0]
        self.ypos += self.velocity[1]

    def info(self):
        print("Particle at " + str(self.xpos) + "," + str(self.ypos) + " with velocity " + str(self.velocity))

#initialization
particles = [Particle(random.randint(0, window_size), random.randint(0, window_size)) for i in range(particle_number)]
particle_coords = []
particle_colours = []
for i in range(len(particles)):
    particle_coords.append(particles[i].xpos)
    particle_coords.append(particles[i].ypos)
for j in range(len(particles)):
    particle_colours.append(random.randint(128, 255))
    particle_colours.append(random.randint(128, 255))
    particle_colours.append(random.randint(128, 255))

def update_physics():
    for particle in particles:
        vector = []
        #vector.append(mouse_coords[0] - particle.xpos)
        #vector.append(mouse_coords[1] - particle.ypos)
        vector.append(window_size / 2 - particle.xpos + 10)
        vector.append(window_size / 2 - particle.ypos)
        magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
        unit_vector = []
        unit_vector.append(2 * vector[0] / magnitude)
        unit_vector.append(2 * vector[1] / magnitude)
        if(mouse_pressed):
            particle.apply_force(unit_vector)
        else:
            #particle.slow()
            particle.velocity = [0, 0]
        global particle_coords
        particle_coords = []
        for i in range(len(particles)):
            particle_coords.append(round(particles[i].xpos))
            particle_coords.append(round(particles[i].ypos))
    

def tick(dt):
    update_physics()
    #window.clear()
    pyglet.graphics.draw(particle_number, pyglet.gl.GL_POINTS, 
        ('v2i', particle_coords),
        ('c3B', particle_colours)
    )

pyglet.clock.schedule_interval(tick, 1/60)
pyglet.app.run()
