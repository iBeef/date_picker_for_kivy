# Date Picker Widget

This widget adds a calendar style date picker to kivy and allows the
user to return the selected date.

By default the open() function of the popup has an argument passed as an object
(parent_obj) which will change the text of the object passed when a date is
selected. This way you can create one date picker popup and change multiple
objects by passing a different object in the open argument opposed to making
a new popup every time.

If you wish to customise the way a date is passed back into the app then
the on_selection property can be easilt modified which is originally passed
a datetime object.

example_usage.py shows how the date picker can be used.

Enjoy!