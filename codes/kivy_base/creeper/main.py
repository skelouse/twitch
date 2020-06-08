from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle
from kivy.config import Config

from sys import platform as sysplatform

if sysplatform == 'linux' or sysplatform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 0)
    Config.set('graphics', 'top', 0)
    Config.set('graphics', 'height', 800)
    Config.set('graphics', 'width', 496)
    #Config.set('graphics', 'height', 420)
    #Config.set('graphics', 'width', 420)
    Config.write()



class ScreenMan(ScreenManager):
    background = 'creep.png'
    def __init__(self, **kwargs):
        super(ScreenMan, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size,
                              pos=self.pos,
                              source=self.background)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
sm = ScreenMan()


class CreepApp(App):
    def build(self):
        sm.add_widget(Screen())
        return sm


if __name__ == "__main__":
    CreepApp().run()