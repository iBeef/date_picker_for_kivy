from kivy.config import Config

Config.set('graphics', 'height', '600')
Config.set('graphics', 'width', '800')

from kivy.app import App

from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from date_picker_widget import CalendarPopup

import os

date_picker_kv = os.path.join('.', 'date_picker_widget.kv')

Builder.load_file(date_picker_kv)
Builder.load_string("""
<ExamplePage>:
    orientation: 'vertical'
    Label:
    Button:
        text: 'Open Popup'
        # Pass the object to recieve the date into the open() call.
        on_release: root.date_picker.open(date_text)
    BoxLayout:
        Label:
            text: 'Date:'
        Label:
            id: date_text
    Label:
""")


class ExamplePage(BoxLayout):


    def __init__(self, **kwargs):
        super(ExamplePage, self).__init__(**kwargs)
        self.date_picker = CalendarPopup(size_hint=(0.8, 0.6))

class ExampleApp(App):


    def build(self):
        return ExamplePage()

if __name__ == '__main__':
    ExampleApp().run()
