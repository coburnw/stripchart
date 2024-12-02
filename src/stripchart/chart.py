import tkinter as tk
import math

class Legend():
    def __init__(self, traces):
        self.traces = traces
        self.index = 0
        return

    def place(self, chart):
        x = chart.width - 50
        y = 50 + self.index*10
        for trace in self.traces:
            text = '{} ({})'.format(trace.title, trace.units)
            chart.create_text(x, y+12*self.index, anchor=tk.SE,
                              text=text, fill=trace.color)
            self.index += 1
        return
        
class Chart(tk.Canvas):
    def __init__(self, root, width, height, background_color, title=''):
        super().__init__(root, width=width, height=height, bg=background_color)
        self.root = root
        self.width = width
        self.height = height
        self.center = self.height//2
        self.title = title

        self.traces = []
        self.scales = []
        self.legend = Legend(self.traces)
        
        self.interval = 0
        return

    def append_scale(self, scale, min=-100, max=100):
        self.scales.append(scale)
        scale.place(self, min, max)
        return
    
    def append_trace(self, trace):
        self.traces.append(trace)
        return

    def update(self, interval_ms=None):
        if interval_ms is not None:
            self.interval = interval_ms

        if self.interval == 0:
            return
        
        for trace in self.traces:
            trace.update(self)
            
        self.root.after(self.interval, self.update)
        return
    
    def show(self):
        self.legend.place(self)
            
        self.pack()
        return
    
if __name__ == '__main__':
    import scale 
    import axis
    import trace
    
    class SineSignal(trace.Trace):
        def __init__(self, x_axis, y_axis, title, initial_value=0, step=1.0/6.28):
            super().__init__(x_axis, y_axis, title)
            self.initial_value = initial_value
            self.step = step
            self.scale = 1
            self.x = 0
            return

        def next_value(self):
            y = self.scale * math.sin(self.x+self.initial_value)
            x = self.x + self.step
            self.x = x
            return (x,y)

    root = tk.Tk()
    root.title('TK StripChart')
    
    chart = Chart(root, 1200, 600, 'white')
    time_axis = axis.HorizontalAxis()
    time_scale = scale.LinearScale(time_axis, position='center', units='Secs')
    chart.append_scale(time_scale, min=0, max=20)

    signal_axis = axis.VerticalAxis()
    volts_scale = scale.LinearScale(signal_axis, position='left', units='Volts')
    chart.append_scale(volts_scale, min=-1.5, max=1.5)
    
    sine = SineSignal(time_scale, volts_scale, title='Line')
    chart.append_trace(sine)
    cosine = SineSignal(time_scale, volts_scale, title='Cross', initial_value=6.28/4)
    chart.append_trace(cosine)
    
    chart.update(500)
    chart.show()

    root.mainloop()
