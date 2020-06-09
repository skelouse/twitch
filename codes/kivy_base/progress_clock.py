from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import CoreLabel
from kivy.graphics import RoundedRectangle, Color
from kivy.clock import Clock


class TInput(TextInput):
    def __init__(self, **kwargs):
        super(TInput, self).__init__(**kwargs)
        self.font_size='60dp'

    def insert_text(self, substring, from_undo=False):
        try:
            int(substring)
        except ValueError:
            pass
        else:
            super(TInput, self).insert_text(substring, from_undo)

class Progress(ProgressBar):
    def __init__(self, **kwargs):
        super(Progress, self).__init__(**kwargs)
        self.label = CoreLabel(
            text='Time Left: ',
            font_size=20)
        self.texture_size = None
        self.refresh_text()
        self.draw()

    def draw(self):

        with self.canvas:
            self.canvas.clear()

            # Draw no progress bar
            Color(.188, .209, .148)
            RoundedRectangle(
                pos=self.pos,
                size=self.size)

            Color(.5, 0, 0)
            if self.value > 0:
                var = 100.0/self.value
                # Draw progress bar
                RoundedRectangle(
                    pos=self.pos,
                    size=(self.width/var, self.height))
            # Center and draw the text
            Color(1, 1, 1, 1)
            RoundedRectangle(texture=self.label.texture, size=self.texture_size,
                pos=(self.size[0]/2 - self.texture_size[0]/2, self.size[1]/2 - self.texture_size[1]/2))

    def refresh_text(self):
        # Render the label
        self.label.refresh()

        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        self.value = value
        self.refresh_text()
        self.size=(400, 30)
        self.draw()
    


class TestApp(App):
    def build(self):
        self.layout = RelativeLayout()
        self.progress = Progress(size=(400, 30), max=100)
        self.progress_relative = RelativeLayout(
            size_hint=(None, None),
            pos_hint={'center_x': .2, 'center_y': .5}
        )
        self.progress_relative.add_widget(self.progress)
        self.layout.add_widget(self.progress_relative)
        self.time_grid = GridLayout(rows=1, pos_hint={'center_x': .5, 'center_y': .9}, size_hint=(.9, .2))

        self.hour = TInput()
        self.minute = TInput()
        self.second = TInput()
        self.time_grid.add_widget(self.hour)
        self.time_grid.add_widget(self.minute)
        self.time_grid.add_widget(self.second)
        self.layout.add_widget(self.time_grid)
        self.btn = Button(text='start timer', pos_hint={'center_x': .5, 'center_y': .1}, size_hint=(.6, .2))
        self.btn.bind(on_press=self.start_time)
        self.layout.add_widget(self.btn)
        return self.layout

    def start_time(self, event):
        self.time = 0
        if self.hour.text:
            self.time += 60*60*int(self.hour.text)
        if self.minute.text:
            self.time += 60*int(self.minute.text)
        if self.second.text:
            self.time += int(self.second.text)

        self.num = 100/self.time
        self.progress.set_value(100)
        self.clock_event = Clock.schedule_interval(self.countdown, 1)

    def countdown(self, dt):
        if self.time == 0:
            self.clock_event.cancel()
        else:
            self.progress.set_value(self.progress.value-self.num)
            self.time -= 1
            self.progress.label.text = ("Time Left: " + str(self.time))
            self.progress.refresh_text()


if __name__ == "__main__":
    TestApp().run()