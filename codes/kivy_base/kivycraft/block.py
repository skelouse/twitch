from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.lang.builder import Builder

from sys import platform as sysplatform
import random


Blocks = {
    'dirt': {
        'color': (0.55, 0.27, 0.07, 1)
    },
    'stone': {
        'color': (0.41, 0.41, 0.41, 1)
    },
    'silver': {
        'color': (0.75, 0.75, 0.75, 1)
    },
    'diamond': {
        'color': (0.44, 0.5, 0.56, 1)
    }  
}
Builder.load_string("""
<Player>:
    canvas:
        Color:
            rgba: 1.0, 0.85, 0.73, 1
        Rectangle:
            pos: self.pos
            size: self.size

<Block>:
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size
""")


class Player(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(-1)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def __init__(self, btype='dirt', **kwargs):
        super(Player, self).__init__(**kwargs)
        self.size = (10, 30)
    def move(self):
        self.pos = Vector(self.velocity) + self.pos

    def walk(self, direction):
        if direction == 'right':
            self.pos[0] += 5
        elif direction == 'left':
            self.pos[0] -= 5
        



class Block(Widget):
    def __init__(self, btype='dirt', **kwargs):
        super(Block, self).__init__(**kwargs)
        self.size=(10, 10)
        self.btype = btype
        with self.canvas.before:
            Color(rgba=Blocks[btype]['color'])


class Game(Widget):
    blocks = []
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.player = Player(pos=(250, 450))
        Clock.schedule_interval(self.update, .01)
        self.generate()
        self.add_widget(self.player)

    def update(self, dt):
        self.player.move()
        self.check_collision()
        
    def check_collision(self):
        for i in self.blocks:
            if self.player.collide_widget(i):
                print('collision')
                if self.player.velocity_y > 0:
                    self.player.velocity_y = 1
                    self.player.pos[1] -= 1
                elif self.player.velocity_y < 0:
                    self.player.velocity_y = 0
                    self.player.pos[1] += 1
                else:
                    if self.player.velocity_x > 0:
                        self.player.pos[0] += self.player.velocity_x
                        self.player.velocity_x = 0
                    else:
                        self.player.pos[0] -= self.player.velocity_x
                        self.player.velocity_x = 0
                    


    def generate(self):
        add = self.addBlock
        x = 0
        y = 0
        for i in range(2200):
            if random.randint(0, 100) < 10 and y < 325:
                add((x, y), 'silver')
            elif random.randint(0, 100) < 3 and y < 24:
                add((x, y), 'diamond')
            elif y < 350:
                add((x, y), 'stone')
            else:
                add((x, y), 'dirt')
            x += 10
            if x == 500:
                x = 0
                y += 10

    def addBlock(self, pos, btype):
        b = Block(pos=pos, btype=btype)
        self.blocks.append(b)
        self.add_widget(b)

class BlockBreak(App):
    def build(self):
        self.game = Game()
        return self.game

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 276:
            self.game.player.walk("left")
        elif key == 273:
            self.game.player.walk("up")
        elif key == 275:
            self.game.player.walk("right")
        elif key == 274:
            self.game.player.walk("down")
        elif key == 119:
            self.game.player.walk("up")
        elif key == 97:
            self.game.player.walk("left")
        elif key == 115:
            self.game.player.walk("down")
        elif key == 100:
            self.game.player.walk("right")
        elif key == 27:
            self.stop()
        return True


if __name__ == "__main__":
    BlockBreak().run()


