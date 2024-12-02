import collections


class Trace():
    def __init__(self, x_scale, y_scale, title='', color='black'):
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.title = title
        self.color = color

        self.is_empty = True
        self.x0 = 0
        self.y0 = 0

        self.segments = collections.deque() # pronounced deck
        return

    @property
    def units(self):
        return self.y_scale.units
    
    def update(self, chart):
        x,y = self.next_value()
        self.append(chart, x, y)
        return
    
    def append(self, chart, x1, y1):
        xy = []

        xy.append(self.x_scale.to_chart(chart, self.x0))
        xy.append(self.y_scale.to_chart(chart, self.y0))

        xy.append(self.x_scale.to_chart(chart, x1))
        xy.append(self.y_scale.to_chart(chart, y1))

        self.x0 = x1
        self.y0 = y1
        
        segment = chart.create_line(xy, fill=self.color)
        self.segments.append(segment)  #then use popleft() to delete
        
        return True

