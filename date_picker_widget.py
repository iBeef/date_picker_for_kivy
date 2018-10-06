from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ListProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager

import calendar
import datetime


# Add kv file into Builder.load_string to package the widget into
# one file.
Builder.load_string("""
<CalendarPopup>:
    BoxLayout:
        id: vert_layout
        orientation: 'vertical'
        padding: dp(15)
        BoxLayout:
            size_hint_y: 0.15
            orientation: 'horizontal'
            Button:
                size_hint_x: 0.25
                text: '<'
                on_release: root.change_year('right')
            Label:
                id: year
                # text: 'year'
            Button:
                size_hint_x: 0.25
                text: '>'
                on_release: root.change_year('left')
        BoxLayout:
            size_hint_y: 0.15
            orientation: 'horizontal'
            Button:
                size_hint_x: 0.25
                text: '<'
                on_release: root.change_month('right')
            Label:
                id: month
                # text: 'month'
            Button:
                size_hint_x: 0.25
                text: '>'
                on_release: root.change_month('left')

<CalendarScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: dp(40)
            orientation: 'horizontal'
            Label:
                text: 'M'
            Label:
                text: 'T'
            Label:
                text: 'W'
            Label:
                text: 'T'
            Label:
                text: 'F'
            Label:
                text: 'S'
            Label:
                text: 'S'
        BoxLayout:
            id: vert_layout
            orientation: 'vertical'

<DateButton>:
    on_release:
        if self.button_month == 'before': \
        self.root.change_month('right')
        # Needs a select function
        if self.button_month == 'current': \
        self.root.select_date(int(self.text))
        if self.button_month == 'after': \
        self.root.change_month('left')
""")


class CalendarPopup(ModalView):


    date = ListProperty()
    direction = StringProperty()
    selection = ObjectProperty()
    parent_obj = ObjectProperty()

    def __init__(self, **kwargs):
        super(CalendarPopup, self).__init__(**kwargs)
        # self.parent_obj = parent_obj
        self.calendar_screens = CalendarScreens()
        self.ids.vert_layout.add_widget(self.calendar_screens)
        self.months_to_num = {v: k for k,v in enumerate(calendar.month_name)}
        self.num_to_months = {k: v for k,v in enumerate(calendar.month_name)}
        self.screen_switch = {'screen_1': 'screen_2', 'screen_2': 'screen_1'}
        # Set date for initial opening of popup
        self.current_date = datetime.datetime.now()
        self.ids.month.text = self.num_to_months.get(self.current_date.month)
        self.ids.year.text = str(self.current_date.year)
        self.calendar_screens.screen_1.update_calendar(
            self.current_date.year,
            self.current_date.month
            )

    def open(self, parent_obj, *largs, **kwargs):
        # Pass in the object that's calling the popup to easily
        # reference it back.
        self.parent_obj = parent_obj
        # Call the original open() function
        super(CalendarPopup, self).open()

    def on_dismiss(self):
        # Shecdule a slight delay to stop the popup reverting to
        # date whilst still open (Looks a lot tidier).
        Clock.schedule_once(self.dismissal, 0.15)

    def dismissal(self, dt):
        # Reset popup to current month for the next time it's opened.
        self.calendar_screens.screen_1.ids.vert_layout.clear_widgets()
        self.calendar_screens.screen_2.ids.vert_layout.clear_widgets()
        self.calendar_screens.current = 'screen_1'
        self.current_date = datetime.datetime.now()
        self.ids.month.text = self.num_to_months.get(self.current_date.month)
        self.ids.year.text = str(self.current_date.year)
        self.calendar_screens.screen_1.update_calendar(
            self.current_date.year,
            self.current_date.month
            )

    def change_month(self, direction):
        # Increase or decrease the month currently showing.
        self.direction = direction
        if direction == 'left':
            if self.months_to_num.get(self.ids.month.text) < 12:
                next_month = self.months_to_num.get(self.ids.month.text) + 1
                self.ids.month.text = self.num_to_months.get(next_month)
            else:
                self.ids.year.text = str(int(self.ids.year.text) + 1)
                self.ids.month.text = 'January'
        else:
            if self.months_to_num.get(self.ids.month.text) > 1:
                next_month = self.months_to_num.get(self.ids.month.text) - 1
                self.ids.month.text = self.num_to_months.get(next_month)
            else:
                self.ids.year.text = str(int(self.ids.year.text) - 1)
                self.ids.month.text = 'December'
        self.date = [
            int(self.ids.year.text),
            self.months_to_num.get(self.ids.month.text),
            ]

    def change_year(self, direction):
        # Increase or decrease the year currently showing.
        self.direction = direction
        if direction == 'left':
            self.ids.year.text = str(int(self.ids.year.text) + 1)
        else:
            self.ids.year.text = str(int(self.ids.year.text) - 1)
        self.date = [
            int(self.ids.year.text),
            self.months_to_num.get(self.ids.month.text),
            ]

    def select_date(self, day):
        # Turn date selection into datetime.datetime format.
        date = datetime.datetime(int(self.ids.year.text),
                self.months_to_num.get(self.ids.month.text), day)
        if self.selection == date:
            self.dismiss()
        else:
            self.selection = date

    def on_direction(self, instance, value):
        # Dynamically change screen transition direction.
        self.calendar_screens.transition.direction = self.direction

    def on_date(self, instance, value):
        # Change between screens to make it look like each month/year
        # has it's own screen.
        self.calendar_screens.current = self.screen_switch.get(
            self.calendar_screens.current_screen.name)

    def on_selection(self, instance, value):
        # Use this function to return date value to main application
        #-----------------------------------------------------------
        # Currently returning the date to the calling objects text
        # variable
        date = datetime.datetime.strftime(self.selection, '%d/%m/%Y')
        self.parent_obj.text = date
        self.dismiss()

class CalendarScreens(ScreenManager):


    def __init__(self, **kwargs):
        super(CalendarScreens, self).__init__(**kwargs)
        self.screen_1 = CalendarScreen(name='screen_1')
        self.screen_2 = CalendarScreen(name='screen_2')
        self.screen_2.first_run = True
        self.add_widget(self.screen_1)
        self.add_widget(self.screen_2)

class CalendarScreen(Screen):


    first_run = BooleanProperty(False)

    def on_pre_enter(self):
        # Refresh calendar before transition animation
        if self.first_run:
            self.update_calendar(self.parent.parent.parent.date[0],
                    self.parent.parent.parent.date[1])

    def on_leave(self):
        # Clear calendar ready for next change
        self.ids.vert_layout.clear_widgets()

    def update_calendar(self, year, month):
        # Input days into calendar
        if self.first_run == False:
            self.first_run = True
        current_month = self.fill_month(year, month)
        month_length = calendar.monthrange(year, month)[1]
        next_month = False
        self.ids.vert_layout.clear_widgets()
        # Date insertion into calendar
        for index, week in enumerate(current_month):
            box = BoxLayout()
            for day in week:
                date_butt = DateButton(text=str(day))
                # Create a reference to main popup widget for each
                # button
                date_butt.root = self.manager.parent.parent
                # If dates from previous month, highlight blue
                if index == 0 and day > 7:
                    date_butt.button_month = 'before'
                    date_butt.background_color = (0, 0, 1, 0.5)
                elif index == len(current_month) - 1 and day == month_length:
                    next_month = True
                # If dates from next month, highlight blue
                if next_month and day != month_length:
                    date_butt.button_month = 'after'
                    date_butt.background_color = (0, 0, 1, 0.5)
                if not date_butt.button_month:
                    date_butt.button_month = 'current'
                box.add_widget(date_butt)
            self.ids.vert_layout.add_widget(box)


    def fill_month(self, year, month):
        # Retrieve a list of all dates within a month and fill gaps
        # around with previous and following months.
        if month == 1:
            month_before = list(calendar.monthcalendar(year - 1, 12))
        else:
            month_before = list(calendar.monthcalendar(year, month - 1))
        if month < 12:
            month_after = calendar.monthcalendar(year, month + 1)
        else:
            month_after = calendar.monthcalendar(year + 1, 1)
        current_month = calendar.monthcalendar(year, month)
        lengths = [len(month_before), len(current_month), len(month_after)]
        # Fill blanks at the start
        for index, day in enumerate(current_month[0]):
            if day == 0:
                current_month[0][index] = month_before[lengths[0] - 1][index]
        # Fill blanks at the end
        for index, day in enumerate(current_month[(lengths[1] - 1)]):
            if day == 0:
                current_month[(lengths[1] - 1)][index] = month_after[0][index]
        return current_month

class DateButton(Button):


        root = ObjectProperty()
        button_month = StringProperty()
