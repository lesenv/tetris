import pygame
import logic

class Block(pygame.sprite.Sprite):
    def __init__(self, color, dim):
        super().__init__()
        self.image = pygame.surface.Surface(dim)
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()
        self.dim = dim
# DEBUGGING
#        print(f"new Block: {color}, {dim}")
        
    def setPos(self, i, j):
        self.rect.topleft = (i*self.dim[0], j*self.dim[1])
# DEBUGGING
#        print(f"new Pos {self.rect.topleft}")
     
    def setPosAbs(self, x, y):
         self.rect.topleft = (x, y)
# DEBUGGING
#         print(f"new PosAbs {self.rect.topleft}")

class Game():
    def __init__(
            self,
            _screen,
            dimension, #of little rect
            px,
            py
            ):
        self.scr = _screen
        self.d, self.px, self.py = dimension, px, py
#        Wenn alles fertig ist, wieder auf False stellen, damit der Startbildschirm startet
#        self.game_active = False
        self.game_active = True
        self.game_logic = logic.Playscreen(self.px, self.py)
# DEBUGGING
#        print("setting up event")
        # timer for falling brick
        self.brick_step = pygame.event.Event(pygame.USEREVENT, mytype="brick_step")
        pygame.time.set_timer(self.brick_step, 300)
        # gathering container of sprites
        self.backgroundSprites = pygame.sprite.Group()
        self.tetrisTilesSprites = pygame.sprite.Group()
        self.setup_background()

    def whileTrue(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ex()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    ex()
                elif event.key == pygame.K_LEFT:
                    self.game_logic.move(logic.MOVE_LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.game_logic.go_right()
                elif event.key == pygame.K_UP:
                    self.game_logic.turn()
                elif event.key == pygame.K_DOWN:
                    self.game_logic.move(logic.MOVE_DOWN)
            elif event.type == pygame.FINGERDOWN:
                if not self.game_active:
                    self.game_active = True
            elif event.type == pygame.USEREVENT:
                if event.mytype == "brick_step":
                    self.game_logic.move(logic.MOVE_DOWN)

        if self.game_active:
            #draw tetris-tiles
            self.draw_tetris(self.game_logic.playscreen)
            #drawing background
            self.backgroundSprites.draw(self.scr)
        else:
            pass
        pygame.display.update()
        timer.tick(60)
        
    def draw_tetris(self, game_matrix):
        # delete all the blocks
        container = self.tetrisTilesSprites
        container.empty()
        self.playscreen.image.fill(self.playscreen.color)
        # finding all the existing blocks
        for j, line in enumerate(game_matrix):
            for i, tile in enumerate(line):
                if tile:
                    t = Block("red", (self.d, self.d))
                    t.setPos(i, j)
                    container.add(t)
        # draw them
        container.draw(self.playscreen.image)
                    
#                    pygame.draw.rect(self.playscreen.image, "red", i*self.d, j*self.d, self.d, self.d)
        
    def setup_background(self):
        '''                              < right >
        _____________ _________________
        |                     | |                           |
        |                     | |   scorescreen  |
        | playscreen | K===========3
        |                     | | previewscreen |
        L___________JL_______________J
        '''
        #background
        self.scr.fill((220,220,120))
        #playscreen
        self.playscreen = Block("Black", (self.d*self.px, self.d*self.py))
        self.playscreen.setPos(1/self.px,1/self.py)
        self.backgroundSprites.add(self.playscreen)
        #right side
        ###scorescreen
        ### (right top)
        box = self.playscreen.rect
        right_start = box.right + self.d
        right_width = self.scr.get_width()- right_start - self.d
        right_top_height = box.height *2/3 - self.d
        self.scorescreen = Block("Black", (right_width, right_top_height))
        self.scorescreen.setPosAbs(right_start, self.d)
        self.backgroundSprites.add(self.scorescreen)
        ###previewscreen
        ### (right bottom)
        right_preview_top = self.scorescreen.rect.bottom + self.d
        right_bottom_height = box.height - right_top_height - self.d
        self.previewscreen = Block("Black", (right_width, right_bottom_height))
        self.previewscreen.setPosAbs(right_start, right_preview_top)
        self.backgroundSprites.add(self.previewscreen)
        

if __name__ == "__main__":
    
    D = 25
    P_X, P_Y = 13, 20
    
    # initialize pygame diplay and variables
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 720, 1438
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    
    timer = pygame.time.Clock()

    g = Game(screen, D, P_X, P_Y)
    while True:
        g.whileTrue()
        pygame.display.update()
        timer.tick(60)
