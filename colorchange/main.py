from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
import random

class ColorApp(App):
    def build(self):
        self.layout = RelativeLayout()
        self.btn = Button(
            background_color=(1, 0, 0, 1)
        )
        
        self.layout.add_widget(self.btn)
        self.btn2 = Button(
            text='Change color',
            pos_hint={'center_x': .5, 'center_y': .1},
            size_hint=(.4, .1)
        )
        self.btn2.bind(on_press=self.change_color)
        self.layout.add_widget(self.btn2)
        return self.layout

    def change_color(self, event):
        color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)
        self.btn.background_color = color

ColorApp().run()
