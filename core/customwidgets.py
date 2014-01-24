from datetime import time
from django.forms import widgets

class TimeSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        hours = [(hour, hour) for hour in range(24)]
        minutes = [(minutes, minutes) for minutes in range(00,60,5)]
        _widgets = (
            widgets.Select(attrs=attrs, choices=hours),
            widgets.Select(attrs=attrs, choices=minutes),
        )
        super(TimeSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.hour, value.minute]
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        timelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            T = time(hour=int(timelist[0]),
            	minute=int(timelist[1])
            )
        except ValueError:
            return ''
        else:
            return str(T)
