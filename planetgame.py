"""
code originally from Peter Collingridge 
http://www.petercollingridge.co.uk/pygame-physics-simulation
https://github.com/petercollingridge/ 
no license information found

adapted by Horst JENS http://github.com/horstjens
"""

import random
import pygame
import particles 
import os
import math

#todo: universe zoom funktion: height und width anpassen auf universe-screen. aber nur bei rauszoomen
#todo: lambdas wegtun bei controller
#todo: trail farben

class UniverseScreen:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        
    def scroll(self, dx=0, dy=0):
        self.dx += dx * width / (self.magnification*10)
        self.dy += dy * height / (self.magnification*10)
        
    def zoom(self, zoom):
        #if zoom ==  2:
            #zoomin.play()
        #elif zoom == 0.5:
         #   zoomout.play()
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
        
    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        
def calculateRadius(mass):
    return 0.5 * mass ** (0.5)


#pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init() 
#fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound
#create = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
#zoomin = pygame.mixer.Sound(os.path.join('data','zoom1.wav'))  #load sound
#zoomout = pygame.mixer.Sound(os.path.join('data','zoom2.wav'))  #load sound

(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))


universe = particles.Environment((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine'])
#universe.addFunctions(['move', 'attract', 'collide', 'combine', 'bounce'])
universe_screen = UniverseScreen(width, height)

#sonne
universe.addParticles(mass=150, size=calculateRadius(150), speed=0, x=300, y=300,
                          colour=(240,225,0))
#for p in range(5):
#    particle_mass = random.randint(10,25)
#    particle_size = calculateRadius(particle_mass)
#    universe.addParticles(mass=particle_mass, size=particle_size, speed=0, 
#                          colour=(random.randint(128,255),
#                                  random.randint(128,255),
#                                  random.randint(128,255)))

#-------------------Sun--------------------
particle_mass = 90
particle_size = calculateRadius(particle_mass)
x = 300
y = 300

px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  

universe.addParticles(mass=particle_mass, size=particle_size, speed=0,
					  colour=(255,255,0),
					  x=px,y=py,angle=0)

#------------------------Mercury-----------------
particle_mass = 10
particle_size = calculateRadius(particle_mass)
x = 250 
y = 250

angle = 15.12*(math.pi/180.0)

px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  

universe.addParticles(mass=particle_mass, size=particle_size, speed=1,
					  colour=(random.randint(0,255),random.randint(0,255),255),
					  x=px,y=py,angle=angle)
#--------------------venus--------------					  
particle_mass = 10
particle_size = calculateRadius(particle_mass)
x = 400 
y = 400

angle = 270*(math.pi/180.0)

px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  

universe.addParticles(mass=particle_mass, size=particle_size, speed=0.3,
					  colour=(random.randint(0,255),random.randint(0,255),255),
					  x=px,y=py,angle=angle)

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.scroll(dx = 1)),
    pygame.K_RIGHT:  (lambda x: x.scroll(dx = -1)),
    pygame.K_DOWN:   (lambda x: x.scroll(dy = -1)),
    pygame.K_UP:     (lambda x: x.scroll(dy = 1)),
    pygame.K_EQUALS: (lambda x: x.zoom(2)),
    pygame.K_KP_MINUS: (lambda x: x.zoom(0.5)),
    pygame.K_MINUS:  (lambda x: x.zoom(0.5)),
    pygame.K_KP_PLUS: (lambda x: x.zoom(2)),
    pygame.K_PLUS:   (lambda x: x.zoom(2)),
    pygame.K_r:      (lambda x: x.reset())}

clock = pygame.time.Clock()
paused = False
running = True
angle=0
while running:
    pygame.display.set_caption('m, +/-, cursor, space. zoom={:.4f} pause={} particles={} angle={:.4f}'.format(universe_screen.magnification, paused, len(universe.particles),angle))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in key_to_function:
                key_to_function[event.key](universe_screen)
            if event.key == pygame.K_5:
                ## create a new star with intitial random speed
                particle_mass = 50
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                
                universe.addParticles(mass=particle_mass, size=particle_size, speed=1,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py,angle=angle)
            if event.key == pygame.K_9:
                ## create a new star with intitial random speed
                particle_mass = 90
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                
                universe.addParticles(mass=particle_mass, size=particle_size, speed=1,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py,angle=angle)
            if event.key == pygame.K_0:
                ## create a new star with intitial random speed
                particle_mass = 400**5
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                
                universe.addParticles(mass=particle_mass, size=particle_size, speed=1,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py,angle=angle)
                          
            if event.key == pygame.K_MINUS:
                print("expand!")
                universe.width *= 2
                universe.height *= 2
            elif event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
            elif event.key == pygame.K_KP6:
                angle= 2 * (2 * math.pi / 8.0)    
            elif event.key == pygame.K_KP2:
                angle= 4 * (2 * math.pi / 8.0)    
            elif event.key == pygame.K_KP3:
                angle= 3 * (2 * math.pi / 8.0)    
            elif event.key == pygame.K_KP4:
                angle= 6 * (2 * math.pi / 8.0)    
            elif event.key == pygame.K_KP1:
                angle= 5 * (2 * math.pi / 8.0)    
            elif event.key == pygame.K_KP7:
                angle= 7 * (2 * math.pi / 8.0)    
            elif event.key == pygame.K_KP8:
                angle= 0 * (2 * math.pi / 8.0)    
            elif event.key == pygame.K_KP9:
                angle= 1 * (2 * math.pi / 8.0)    
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: # scrollwheel up
                key_to_function[pygame.K_PLUS](universe_screen)
            elif event.button == 5: # scrollweeel down
                key_to_function[pygame.K_MINUS](universe_screen)
            elif event.button == 1:
            
                # create a new star without speed
                particle_mass = random.randint(1,1)
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                
                 
                universe.addParticles(mass=particle_mass, size=particle_size, speed=0,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py)
            elif event.button == 3:
                # create a new star with intitial random speed
                particle_mass = random.randint(1,1)
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                
                universe.addParticles(mass=particle_mass, size=particle_size, speed=2+random.random()*1.0,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py,angle=angle)


    if not paused:
        universe.update()
        
    screen.fill(universe.colour)
    # ---- paint trail of destroyed stars ----
    for minilist in universe.history:
            color = len(minilist)
            for pos in minilist:
                hx = pos[0]
                hy = pos[1]
                hx = int(universe_screen.mx + (universe_screen.dx + hx) * universe_screen.magnification)
                hy = int(universe_screen.my + (universe_screen.dy + hy) * universe_screen.magnification)
                pygame.draw.rect(screen, (255-min(color, p.colour[0]), 255-min(color, p.colour[1]), 255-min(color, p.colour[2])), (hx, hy, 2,2))
            del minilist[0]
    universe.history = [li for li in universe.history if len(li)>0] # cleanup lost trail history
    
    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']
        # --- paint star trail ----
        color = 255
        for pos in p.history:
            hx = pos[0]
            hy = pos[1]
            hx = int(universe_screen.mx + (universe_screen.dx + hx) * universe_screen.magnification)
            hy = int(universe_screen.my + (universe_screen.dy + hy) * universe_screen.magnification)
            #print(color, p.colour, hx, hy)
            pygame.draw.rect(screen, (255-min(color, p.colour[0]), 255-min(color, p.colour[1]), 255-min(color, p.colour[2])), (hx, hy, 2,2))
            color-= 1
        
        # paint star itself
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * universe_screen.magnification)
        y = int(universe_screen.my + (universe_screen.dy + p.y) * universe_screen.magnification)
        size = int(p.size * universe_screen.magnification)

        
                
        if size < 2:
            pygame.draw.rect(screen, p.colour, (x, y, 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (x, y), size, 0)
        
      
    
    for p in particles_to_remove:
        if p.mass > 3:  # impact shards at collision of big planets
            for impact in range(5, 10):
                mass = 1
                size = calculateRadius(mass)
                #universe.addParticles(mass=mass, size=size, speed=1+random.random()* 2.0,
                 #                         colour=(255,0,0),x=p.x,y=p.y)

        if p in universe.particles:
            universe.history.append(p.history)
            universe.particles.remove(p)
            #fail.play()

    pygame.display.flip()
    clock.tick(80)
