import tkinter as tk


class Legend():
    def __init__(self, traces):
        self.traces = traces
        self.index = 0
        return

    def place(self, chart):
        x = chart.width * 0.75
        y = 50 - self.index*10
        for trace in self.traces:
            if trace.label is not None:
                text = '{} ({})'.format(trace.label, trace.units)
                chart.create_text(x, y+12*self.index, anchor=tk.SE, text=text, fill=trace.color)
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

    def append_scale(self, scale, min_value, max_value):
        self.scales.append(scale)
        scale.place(self, min_value, max_value)
        return
    
    def append_trace(self, trace):
        self.traces.append(trace)
        return

    def update(self, interval_ms=None):
        for trace in self.traces:
            trace.update(self)
            
        # chart updates itself if interval is set larger than 0.
        if interval_ms is not None:
            self.interval = interval_ms

        if self.interval > 0:
            self.root.after(self.interval, self.update)

        return
    
    def show(self, legend=False):
        if legend is True:
            self.legend.place(self)
            
        self.pack(expand=True, fill='both')
        return
