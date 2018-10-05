from kivy.config import Config

Config.set('graphics', 'height', '600')
Config.set('graphics', 'width', '800')

from kivy.app import App

from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from date_picker_widget import CalendarPopup

Builder.load_string("""
<ExamplePage>:
    orientation: 'vertical'
    Label:
    BoxLayout:
        orientation: 'horizontal'
        # Pass the object to recieve the date into the open() call.
        Button:
            text: 'Set Label 1 date'
            on_release: root.date_picker.open(date_text)
        Button:
            text: 'Set Label 2 date'
            on_release: root.date_picker.open(another_date_text)
    BoxLayout:
        Label:
            text: 'Label 1 date:'
        Label:
            id: date_text
        Label:
            text: 'Label 2 date:'
        Label:
            id: another_date_text
    Button:
        text: 'Change this text'
        on_release: root.date_picker.open(self)
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
