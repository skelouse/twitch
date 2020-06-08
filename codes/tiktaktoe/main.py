from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label


class TikApp(App):
    x_is_choose = 1
    def build(self):
        self.layout = RelativeLayout()
        self.grid = GridLayout(
            cols=3,
            pos_hint={'center_y': .7},
            size_hint=(1, .7)
            )
        for i in range(9):
            btn = Button(
                font_size='60dp'
            )
            btn.bind(on_press=self.add_xy)
            self.grid.add_widget(btn)
        self.layout.add_widget(self.grid)

        self.label = Label(
            text="X is choosing",
            pos_hint={'center_y': .2},
            font_size='40dp'
        )
        self.layout.add_widget(self.label)

        self.restartbtn = Button(
            text='Restart',
            pos_hint={'center_y': .1, 'center_x': .5},
            font_size='40dp',
            size_hint=(.8, .1)

        )
        self.restartbtn.bind(on_press=self.restart)
        return self.layout

    def restart(self, event):
        self.label.text = 'X is choosing'
        for i in self.grid.children:
            i.text = ''
            self.x_is_choose = 1
        self.layout.remove_widget(self.restartbtn)


    def add_xy(self, event):
        if not event.text:
            if self.x_is_choose:
                self.x_is_choose = 0
                self.label.text = 'Y is choosing'
                event.text = 'X'
                event.color = (1, 0, 0, 1)
            else:
                self.x_is_choose = 1
                self.label.text = 'X is choosing'
                event.text = 'Y'
                event.color = (0, 0, 1, 1)

            self.check_win()

    def check_win(self):
        
        s = []
        for i in self.grid.children:
            s.append(i.text)

        r1 = s[0:3]
        r2 = s[3:6]
        r3 = s[6:]

        c1 = [s[0], s[3], s[6]]
        c2 = [s[1], s[4], s[7]]
        c3 = [s[2], s[5], s[8]]

        d1 = [s[0], s[4], s[8]]
        d2 = [s[2], s[4], s[6]]

        sequences = [r1, r2, r3, c1, c2, c3, d1, d2]
        for i in sequences:
            x = 0
            y = 0
            for k in i:
                if k == 'X':
                    x += 1
                elif k == 'Y':
                    y += 1
            if x == 3:
                self.win('X')
            elif y == 3:
                self.win('Y')

        blank = False
        for i in s:
            if i == '':
                blank = True
        if not blank:
            self.win('Cat')
# 0 1 2
# 3 4 5
# 6 7 8

    def win(self, letter):
        self.label.text = (letter+" wins!!!")
        self.layout.add_widget(self.restartbtn)


if __name__ == "__main__":
    TikApp().run()