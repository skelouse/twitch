from kivy.app import App

from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.graphics import Rectangle
from kivy.clock import Clock

from kivy.uix.widget import Widget

from functools import partial
import random

class Food(Widget):
    def __init__(self, x, y, **kwargs):
        super(Food, self).__init__(**kwargs)
        self.pos = (x, y)


class SnakeGame(Widget):
    score = NumericProperty(0)
    food = []
    segments = []
    new_segments = []
    food_timer = 0
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def update(self, dt):
        self.food_timer += 1
        if self.food_timer == 100:
            #print(self.app.snake.eat())
            self.plant_food()
            self.food_timer = 0
            #self.app.snake.eat()
        
        for f in self.food:
            if self.app.snake.collide_widget(f):
                self.remove_widget(f)
                self.food.remove(f)
                self.app.snake.eat()

        self.app.snake.move()
        for i in self.segments:
            i.move()


    def plant_food(self):
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        f = Food(x, y)
        self.food.append(f)
        self.add_widget(f)


class PlayerSnake(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    child = None
    _parent = None

    def move(self):
        self.pos = Vector(self.velocity) + self.pos

    def turn(self, direction, *dt):
        if direction == "right":
            self.velocity = (1, 0)
        elif direction == "left":
            self.velocity = (-1, 0)
        elif direction == "down":
            self.velocity = (0, -1)
        elif direction == "up":
            self.velocity = (0, 1)
        if self.child:
            Clock.schedule_once(partial(self.child.turn, direction), .155)
        self.align()
    def align(self):
        if self._parent:
            v = [element * 13 for element in self._parent.velocity]
            x = self._parent.pos[0] - v[0]
            y = self._parent.pos[1] - v[1]
            self.pos = [x, y]
            self.velocity = self._parent.velocity


    def eat(self):
        # self.parent is game
        if not self.child:
            # Make first child separate for collision
            self.parent.score += 1
            v = [element * 13 for element in self.velocity]
            x = self.pos[0] - v[0]
            y = self.pos[1] - v[1]
            new_seg = PlayerSnake()
            new_seg.pos = [x, y]
            new_seg.velocity = self.velocity
            self.child = new_seg
            self.child._parent = self
            self.parent.add_widget(new_seg)
            self.parent.segments.append(new_seg)
        else:
            self.child.eat()

class SnakeApp(App):
    def hook_keyboard(self, window, key, *largs):
        if key == 276:
            self.snake.turn("left")
        elif key == 273:
            self.snake.turn("up")
        elif key == 275:
            self.snake.turn("right")
        elif key == 274:
            self.snake.turn("down")
        elif key == 119:
            self.snake.turn("up")
        elif key == 97:
            self.snake.turn("left")
        elif key == 115:
            self.snake.turn("down")
        elif key == 100:
            self.snake.turn("right")
        elif key == 27:
            self.stop()
        return True

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def build(self):
        self.game = SnakeGame()
        self.snake = PlayerSnake()
        self.snake.velocity_x = 1
        self.game.add_widget(self.snake)
        Clock.schedule_interval(self.game.update, .01)
        return self.game

if __name__ == "__main__":
    SnakeApp().run()