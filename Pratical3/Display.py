def draw_particles(particles):
    draw_square()
    print("drawParticles:" + str(transform_particles(particles)))

#transform the particles (x,y) coordinates to suitable screen coordinates
def transform_particles(particles):
    return [(200 + (x * 10), 200 + (y * 10), theta) for (x,y,theta) in particles]


#draws the square to the display
def draw_square():
    print("drawLine:", str((200,200,200,600)))
    print("drawLine:", str((200,600,600,600)))
    print("drawLine:", str((600,600,600,200)))
    print("drawLine:", str((600,200,200,200)))
    
