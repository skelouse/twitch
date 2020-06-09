from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.lang.builder import Builder

from functools import partial
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
        self.size = (5, 15)
    def move(self):
        self.pos = Vector(self.velocity) + self.pos

    def walk(self, direction, *dt):
        if direction == 'right':
            self.step(1, 0)
        elif direction == 'left':
            self.step(-1, 0)

    def step(self, x, y):
        print("stepping", x, y)
        self.pos[0] += x
        self.pos[1] += y

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
        self.block_broken = False

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

    def break_block(self, block, *dt):
        self.blocks.remove(block)
        self.remove_widget(block)
                    


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

class TempWidget(Widget):
    def __init__(self, **kwargs):
        super(TempWidget, self).__init__(**kwargs)
        self.size=(5, 1)

class BlockBreak(App):
    #walking_events = []
    def build(self):
        self.game = Game()
        return self.game

    def on_start(self):
        from kivy.core.window import Window
        self.block_broken = False
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)
        self.walk_left_event = Clock.schedule_interval(partial(self.game.player.walk, 'left'), .01)
        self.walk_right_event = Clock.schedule_interval(partial(self.game.player.walk, 'right'), .01)
        self.walk_left_event.cancel()
        self.walk_right_event.cancel()

    def _keyboard_closed(self, *args):
        pass

    def on_keyboard_down(self, keyboard, key, *largs):
        print(key, 'down')
        key = key[0]
        if key == 276 or key == 97:
            if not self.walk_left_event.is_triggered:
                self.game.player.walk('left')
            self.walk_left_event()
        elif key == 273 or key == 119:
            self.jump_event()
        elif key == 275 or key == 100:
            if not self.walk_right_event.is_triggered:
                self.game.player.walk('right')
            self.walk_right_event()
        elif key == 274 or key == 115:
            self.go_down_event()
        elif key == 27:
            self.stop()
        return True
        
    def jump_event(self):
        self.game.player.pos[1] += 1

    def go_down_event(self):
        block_break_time = .5
        # find a block below player
        for block in self.game.blocks:
            if TempWidget(pos=(self.game.player.pos[0], self.game.player.pos[1] - 1)).collide_widget(block) and not self.block_broken:
                self.game.player.velocity_y = -1
                self.game.break_block(block)
                self.block_broken = True
                Clock.schedule_once(self.finish_break, block_break_time)

    def finish_break(self, dt):
        self.block_broken = False
        
    def on_keyboard_up(self, keyboard, key, *largs):
        key = key[0]
        if key == 276 or key == 97:
            self.walk_left_event.cancel()
        elif key == 273 or key == 119:
            self.jump_event()
        elif key == 275 or key == 100:
            self.walk_right_event.cancel()
        elif key == 274 or key == 115:
            self.go_down_event()
        elif key == 27:
            self.stop()
        return True



if __name__ == "__main__":
    BlockBreak().run()


