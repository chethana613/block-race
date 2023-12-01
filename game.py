import pygame
from network import Network
import time
import ast


class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color

    def draw(self, g, flag=False):
        if flag:
            self.color = (0,255,0)
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)




    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def setup_canvas(self):
        canvas_text = "Block Race"
        self.canvas = Canvas(self.width, self.height, canvas_text)

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(100,100)
        self.color=(0,0,255)
        if(self.net.connected):
            print("starting game")
            self.setup_canvas()

    def run(self):
        clock = pygame.time.Clock()
        run = True
        flag = False
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)
                    if(self.player.x == 0 and self.player.y == 0):
                        print("winner")
                        flag = True


            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)
                    if(self.player.x == 0 and self.player.y == 0):
                        print("winner")
                        flag = True

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)
                    if(self.player.x == 0 and self.player.y == 0):
                        print("winner")
                        flag = True

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)
                    if(self.player.x == 0 and self.player.y == 0):
                        print("winner")
                        flag = True

            # Send Network Stuff
            self.player2.x, self.player2.y, self.player2.color = self.parse_data(self.send_data(flag), (0,0,255))
            
            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas(), flag)
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()
            if flag:
                time.sleep(5)
                run = False

        pygame.quit()
    

    def send_data(self, flag):
        """
        Send position to server
        :return: None
        """
        if flag:
            color = (3,3,3)
        else:
            color = (255,193,37)
        data = str(self.net.id) + ":" + str(self.player.x) + "|" + str(self.player.y) + "|" + str(color)

        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data, color):
        try:
            d = data.split(":")[1].split("|")
            # if len(d)==3:
            #     self.color = d[2]
            if len(d)==3:
                color = ast.literal_eval(d[2])
            return int(d[0]), int(d[1]), color


        except Exception as e:
            return 50,50, color


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))