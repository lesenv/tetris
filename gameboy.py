import snake, tetris

import pygame


class Gameboy():
    def __init__(self,
                         scr,
                         DIM = 20):
        # getting screen and dimension of givens
        self.scr = scr
        self.DIM = DIM
        # calculate playscreen coords
        self.PLAY_X = int(self.scr.get_width()/self.DIM*7/8)
        self.PLAY_Y = int(self.scr.get_height()/self.DIM/2)
        self.playscreen = pygame.Surface((self.DIM*self.PLAY_X, self.DIM*self.PLAY_Y))
        self.playscreen_rect = self.playscreen.get_rect(midtop = (self.scr.get_width()/2, self.DIM))
        # fontsize
        font_size = int((self.scr.get_height() - self.playscreen_rect.bottom)/10)
        self.font_ab = pygame.font.Font(None, font_size)
        # drawing background
        self.scr.fill((120, 120, 120))
        self.buttons_dir = []
        self.buttons_ab = []
        self.buttons = []
        self.draw()
        
    def draw(self):
        self.draw_buttons()
        self.draw_gamescreen()
        
    def draw_gamescreen(self):
        borderwidth = 10
        border_rect = self.playscreen.get_rect()
        border_rect.width += 2*borderwidth
        border_rect.height += 2*borderwidth
        border_rect.center = self.playscreen_rect.center
        pygame.draw.rect(self.scr, "White", border_rect, width=10)

        
    def draw_buttons(self):
        #cross for directions
        big = (self.scr.get_height() - self.playscreen_rect.bottom)/8
        j = self.scr.get_height() - self.playscreen_rect.bottom / 2
        i = self.playscreen_rect.left + big
        pygame.draw.circle(
            self.scr,
            "Lightgrey",
            (i+big/2, j+big/2),
            big*2)
        down = pygame.draw.rect(
            self.scr,
            "Black",
            (i,j+big, big, big))
        up = pygame.draw.rect(
            self.scr,
            "Black",
            (i, j-big, big, big))
        left = pygame.draw.rect(
            self.scr,
            "Black",
            (i-big, j, big, big))
        right = pygame.draw.rect(
            self.scr,
            "Black",
            (i+big, j, big, big))
        self.buttons_dir = [up, right, down, left]
        #A and B
        x = self.playscreen_rect.right - big
        y = self.scr.get_height() - self.playscreen_rect.bottom / 3
        a = pygame.draw.circle(
            self.scr,
            "Red",
            (x-big, y),
            big/2)
        b = pygame.draw.circle(
            self.scr,
            "Red",
            (x, y-big),
            big/2)
        self.buttons_ab = [a, b]
        self.buttons = self.buttons_dir + self.buttons_ab
        atxt = pygame.transform.rotate(self.font_ab.render("A", None, "Black"), 45)
        atxt_rect = atxt.get_rect(center=a.center)
        self.scr.blit(atxt, atxt_rect)
        btxt = pygame.transform.rotate(self.font_ab.render("B", None, "Black"), 45)
        btxt_rect = btxt.get_rect(center=b.center)
        self.scr.blit(btxt, btxt_rect)
    
    def detect_buttons(self, point):
        '''return if given point in buttons'''
        if pygame.Rect(point).collidelistall(self.buttons):
            return True
        return False
        
    def which_button(self, point):
        '''return specific button pointed at'''
        for but in self.buttons:
            if pygame.Rect(point).colliderect(but):
                if but in self.buttons_dir:
                #directions
                    return self.fingercross(but)
                elif but in self.buttons_ab:
                #ab
                    return self.fingerab(but)
        return None
        
    def fingercross(self, button):
        '''redirect cross to arrows on keyboard'''
        if button == self.buttons_dir[0]:
            return pygame.K_UP
        if button == self.buttons_dir[1]:
            return pygame.K_RIGHT
        if button == self.buttons_dir[2]:
            return pygame.K_DOWN
        if button == self.buttons_dir[3]:
            return pygame.K_LEFT
        return None
            
    def fingerab(self, button):
        '''a = SPACE, b = ENTER/RETURN'''
        if button == self.buttons_ab[0]:
            return pygame.K_SPACE
        if button == self.buttons_ab[1]:
            return pygame.K_RETURN
        return None
##class Gameboy END
# initialize pygame diplay and variables
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 1438
SCREEN_WIDTH, SCREEN_HEIGHT = 360, 719
SCREEN_WIDTH, SCREEN_HEIGHT = 550, 1000
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
timer = pygame.time.Clock()
# instancing of gameboy and game (still just one game)
gb = Gameboy(screen)
## snake
#g = snake.Game(
## tetris
g = tetris.Game(
    gb.playscreen,
    gb.DIM)
    
# whiletrue loop
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ex()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    ex()
                else:
                    pygame.event.post(event)
            elif event.type == pygame.FINGERDOWN:
                # making a little 1by1-rectangle around the finger-point
                posRect = (
                    event.x*SCREEN_WIDTH,
                    event.y*SCREEN_HEIGHT, 1, 1)
                # if clicked on either gameboy-button,
                # post a KEYDOWN-event for the
                # next loop of the game_whileTrue
                if gb.detect_buttons(posRect):
                    new_move = pygame.event.Event(
                           pygame.KEYDOWN,
                           {
                              'unicode': '',
                              'key': gb.which_button(posRect),
                              'mod': 0,
                              'scancode': 80,
                              'window': None
                           })
                    pygame.event.post(
                       new_move
                    )
                else:
                    print("another button:", event)
                    pygame.event.post(event)
        # after event-loop, draw the gameboy
        gb.draw()
        screen.blit(gb.playscreen, gb.playscreen_rect)
        # one step of game-while_True
        g.whileTrue()
        pygame.display.update()
        timer.tick(60)
