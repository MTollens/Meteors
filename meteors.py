import pygame
import colorsLib as cass
import random
import time
pygame.init()
display_width = 800
display_height = 600
fps = 30
smallText = pygame.font.Font("SCR.otf", 20)
paused = False
version = "1.0.0"
"""
author: 
Matthew Thompson
version 1.0.0
"""

#a simple 2 dimensional object manager
class XY:
    def __init__(self, x, y):
        for a in [x, y]:
            assert isinstance(a, int), "not an int"
        self.x = x
        self.y = y

        #takes in an XY class and adds it to the current class
    def add(self, update):
        assert isinstance(update, XY), 'update is not an XY class'
        self.x += update.x
        self.y += update.y

    #returns the contents in the form of a list, for drawing functions
    def to_list(self):
        return (self.x, self.y)

    def __mul__(self, other):
        assert isinstance(other, int), "other is not an int"
        return XY(self.x * other, self.y * other)


def create_timings(filename):
    pass


class Level:
    def __init__(self, advance, fail, timings, special=None):

        #upon completing the level, the next level will be the one signified by "advance"
        self.advance = advance
        #upon failure the level resorts to the level signified by "fail"
        self.fail = fail

        #the "Timings" is a dictionary where the key is the time, and the lookup is the event that happens
        assert isinstance(timings, dict), "the 'timings' argument must be a dictionary"
        self.timings = timings

        #the "special" is a set of instructions for before, during, and after, a round.
        #such as: health change, weapon change, etc...
        self.special = special

    def __getitem__(self, item):
        if item in self.timings:
            return self.timings[item]
        else:
            return False


def meteor_color():
    return cass.meteor[random.randint(0, len(cass.meteor) - 1)]


def star_color():
    return cass.stars[random.randint(0, len(cass.stars) - 1)]


class Physics:
    def __init__(self, x=0, y=0, xv=0, yv=0, xa=0, ya=0):
        self.position = XY(x, y)
        self.velocity = XY(xv, yv)
        self.acceleration = XY(xa, ya)
        self.garbage = False

    def position_update(self, multiplier=None):
        if not multiplier:
            multiplier = 1
        self.position.add(self.velocity * multiplier)
        self.velocity.add(self.acceleration * multiplier)


class Meteor(Physics):
    def __init__(self, x, y, s, M, E, health):
        #physics information
        Physics.__init__(self, x, y)

        #physical size, also hitbox
        self.size = s

        #for the following 2 values, a 0 means no reactance, positive numbers are a positive correlation,
        # and negative is negative correlation

        #magnetic field reactance
        self.magnetic = M

        #electric field reactance
        self.electric = E

        #the actual color
        self.color = meteor_color()

        #when true will be deleted in a garbage collection
        self.delete = False

        #health points to go through until destroyed
        self.health = health

    def collision(self):
        pass

    def destroyed(self):
        #this handles all the visual and score counting and such
        pass

    def attracted(self, magnetism, electrical):
        pass

    def Hit_base(self):
        pass

    def draw(self):
        if abs(self.position.x + self.size) > display_width/2:
            self.delete = True
            pass

        if abs(self.position.y + self.size) > display_height:
            pass
        pygame.draw.circle(gameDisplay, self.color, self.position.to_list(), self.size)
        pygame.draw.circle(gameDisplay, self.color, self.position.to_list(), self.size)


class Bullet(Physics):
    def __init__(self, x, y, size, shape, color, M, E, penetration):

        #physics information
        Physics.__init__(x, y)

        # physical size, also hitbox
        self.size = size

        # for the following 2 values, a 0 means no reactance, positive numbers are a positive correlation,
        # and negative is negative correlation

        #when 1 is circle, when 2 is line/ rectangular
        self.shape = shape
        # magnetic field reactance
        self.magnetic = M

        # electric field reactance
        self.electric = E

        self.color = color

        # when true will be deleted in a garbage collection
        self.delete = False

        # number of times projectile can damage something
        self.penetration = penetration


class Particle(Physics):
    def __init__(self,color, life, size, x, y, x_vel, y_vel):
        self.color = color
        #deincrements once per frame, deleted once offscreen
        self.life = life
        self.size = size
        Physics.__init__(x, y, x_vel, y_vel)
        self.delete = False

    def cycle(self):
        self.deletecheck()
        self.draw()


    def deletecheck(self):
        if self.delete:
            pass

        if self.position.x_val():
            pass


    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, self.position.to_list(), self.size)




class star:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, [self.x, self.y], 1)


def quitgame():
    pygame.quit()
    quit()


next_load = 1


def load_level():
    pass

#bullets and meteors
objects = [1, 1, 1]
#x, y, s, M, E, health):
objects[0] = Meteor(200, 300, 5, 1, 1, 1)
objects[1] = Meteor(100, 100, 5, 1, 1, 1)
objects[2] = Meteor(100, 400, 5, 1, 1, 1)
#particles
particles = []
#stars
stars_on = True
stars = []
global M
global E
M = 0
E = 0


def field_toggle(field, direction):
    if direction > 0:
        field = 1
    elif direction < 0:
        field = -1
    elif direction == 0:
        field = 0
    return field


def stars_generate(number_of_stars):
    for x in range(0, number_of_stars):
        stars.append(star(random.randint(0, display_width), random.randint(0, display_height), star_color()))


def stars_reset():
    global stars
    stars = []


particle_limit = 100


def field_color(M, E):
    if M > 0:
        if E > 0:
            return cass.orange
        if E == 0:
            return cass.red
        if E < 0:
            return cass.purple
    if M == 0:
        if E > 0:
            return cass.item_yellow
        if E == 0:
            return cass.black
        if E < 0:
            return (75, 56, 75)
    if M < 0:
        if E > 0:
            return cass.green
        if E == 0:
            return cass.light_blue
        if E < 0:
            return cass.blue


def draw(timing):
    #background
    gameDisplay.fill(cass.black)

    #field
    pygame.draw.circle(gameDisplay, cass.add_alpha(cass.muted(field_color(M,E), .2), 255), (int(display_width/2), int(display_height)), int(display_width*.5))

    #stars
    if stars_on:
        for s in range(1, stars.__len__()):
            stars[s].draw()

    #objects
    global objects
    for obj in objects:
        obj.draw()

    """
    for x in range(0, particle_limit):
        particles[x].draw()

    #foreground
    """


def physics(timing):
    for obj in objects:
        #assert isinstance(object, Physics), "object is not a physics thing"
        obj.position_update(timing)

    """
    for particle in particles:
        assert isinstance(particle, Particle), "not a particle"
        particle.position_update(timing)
    """

def slowfuzz():
    for x in range(0, display_width):
        pygame.display.update()
        for y in range(0,display_height):
            fill = cass.black
            for modifierx in range(-1,2):
                for modifiery in range(-1,2):
                    x2 = x + modifierx
                    y2 = y + modifiery
                    if x2 not in range(0, display_width):
                        x2 = 0
                    if y2 not in range(0, display_height):
                        y2 = 0
                    val = cass.remove_alpha(gameDisplay.get_at((x2, y2)))
                    print("debug {} {} {} {} {} {}".format(x2, y2, modifierx, modifiery, cass.tohex(fill), val))
                    fill = cass.add(fill, val)
            pygame.display.update()
            gameDisplay.set_at((x, y), cass.average(fill, 9))
    pygame.display.update()


def text_objects(text, font, color=None):
    if not color:
        color = cass.black
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()


# message, x, y, width, height, color, clicked color
def button(msg, x, y, w, h, ic, ac=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    send = False
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if not ac:
            ac = cass.muted(ic)
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1:
            send = True
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)
    return send


def pause_menu():
    global paused
    paused = True
    # background
    gameDisplay.fill(cass.grey)
    # stars
    if stars_on:
        for s in range(1, stars.__len__()):
            stars[s].draw()
    pygame.display.update()
    while True:
        if button("unpause 'P'", display_width/2 - 200, display_height/2, 200, 60, cass.pink):
            paused = False

        if button("Info", display_width/2, display_height/2, 200, 60, cass.green):
            print("info goes here")
            time.sleep(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    paused = False

        if paused == False:
            break
        pygame.display.update()


def random_color():
    return cass.all_colors[random.randint(0, len(cass.all_colors) -1)]


def main_menu():
    target_color = [0, 0, 0]
    next_color = random_color()
    a = 0
    while True:
        a += 1
        if a >= 20:
            for x in range(0, 2):
                if target_color[x] < next_color[x]:
                    target_color[x] += 1
                elif target_color[x] == next_color[x]:
                    next_color = random_color()
                elif target_color[x] > next_color[x]:
                    target_color[x] += -1
            a = 0


        gameDisplay.fill(cass.muted(target_color, .5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    break

        if button("level {}".format(next_load), display_width/2 - 100, display_height/2, 200, 60, cass.pink):
            break

        if button("Info", display_width/2 - 100, display_height -200, 200, 60, cass.green):
            print("info goes here")
            time.sleep(2)

        if button("Exit", (display_width/2) - 100, display_height -70, 200, 60, cass.dark_red):
            quitgame()

        pygame.display.update()


# gameloop
if __name__ == "__main__":
    stars_generate(100)
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('magnetic meteors')
    clock = pygame.time.Clock()
    main_menu()
    while True:
        #one loop is the game loop, the other is for the loading of new levels

        while True:

            #control input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitgame()


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = True
                        pause_menu()

                    if event.key == pygame.K_ESCAPE:
                        paused = True
                        pause_menu()

                    if event.key == pygame.K_a:
                        M = field_toggle(M, -1)
                    if event.key == pygame.K_s:
                        M = field_toggle(M, -0)
                    if event.key == pygame.K_d:
                        M = field_toggle(M, 1)

                    if event.key == pygame.K_q:
                        E = field_toggle(E, -1)
                    if event.key == pygame.K_w:
                        E = field_toggle(E, 0)
                    if event.key == pygame.K_e:
                        E = field_toggle(E, 1)

            physics(0)

            draw(0)

            #garbage collection


            pygame.display.update()  # shows all the things you have previously drawn ^^^^^
            clock.tick(fps)
