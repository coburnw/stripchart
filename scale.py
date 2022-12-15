import math

import tkinter as tk

class Tick():
    def __init__(self, coefficient, exponent):
        self._coefficient = coefficient
        self._exponent = exponent
        return

    def __repr__(self):
        return 'coef={},exp={} for {}'.format(
            self.coefficient,self.exponent, self.value)
        
    @property
    def value(self):
        val = self._coefficient * pow(10,self._exponent)
        return val
    
    @property
    def coefficient(self):
        return self._coefficient

    @property
    def exponent(self):
        return self._exponent

    @property
    def mark(self):
        pass

class TickRange():
    def __init__(self, min_val, max_val):
        #self.bipolar = bipolar
        
        coef,exp = self.split(max_val)    
        max_tick,tick_count = self.upper(coef)
        self.tmax = Tick(max_tick, exp)
        print(self.tmax)
        self.step = self.tmax.value/tick_count

        coef,exp = self.split(min_val)    
        min_tick,tick_count = self.upper(coef)
        self.tmin = Tick(min_tick, exp)
        return

    def __repr__(self):
        return 'ticks from {} to {} step {}'.format(
            self.tmin.value, self.tmax.value, self.step)
    
    def split(self, value, exponent=None):
        if exponent is None:
            id = 'e'
            str = '{:e}'.format(value)
            coef,sep,exp = str.partition(id)
        else:
            exp = exponent
            coef = value/10**exp

        return (float(coef), int(exp))

    def upper(self, value):
        #sequence is a list of (max-tick-val, numb-of-ticks)
        sequence = [(0,4),(1,4),(2,4),(3,3),(4,4),(5,5),(6,3),(8,4),(8,4),(10,4),(10,4)]

        sign = math.copysign(1, value)
        ceil = math.ceil(abs(value))

        tvalue,count = sequence[ceil]
        tvalue = tvalue * sign
        return tvalue, count
        
    @property
    def spread(self):
        return self.tmax.value - self.tmin.value

    def ticks(self):
        start = self.tmin.value
        stop = self.tmax.value
        accum = start
        while accum <= stop:
            coef,exp = self.split(accum, self.tmax.exponent)
            tick = Tick(coef, exp)
            accum += self.step
            yield tick

        return
    
class Scale():
    def __init__(self, axis, position, units, color):
        self._axis = axis
        self.pos = position
        self.units = units
        self.color = color

        if self.pos not in ['left', 'right', 'top', 'center', 'bottom']:
            raise ValueError

        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0
        self.bipolar_offset = 0

        return

    @property
    def axis(self):
        return self._axis.axis
    
    def place(self, chart, min, max):
        print('{}-scale place: min={}, max={}'.format(self.axis, min,max))
        self.range = TickRange(min, max)
        
        self.left_margin = 0.1 * chart.width
        self.right_margin = 0.9 * chart.width
        self.top_margin = 0.1 * chart.height
        self.bottom_margin = 0.9 * chart.height
        self.bipolar_offset = chart.height / 2

        if self.axis == 'y':
            y0 = self.top_margin
            y1 = self.bottom_margin
            self.length = y1-y0
            if self.pos == 'left':
                x0 = self.left_margin
                x1 = self.left_margin
            elif self.pos == 'right':
                x0 = self.right_margin
                x1 = self.right_margin
        else:
            x0 = self.left_margin
            x1 = self.right_margin
            self.length = x1-x0
            if self.pos == 'top':
                y0 = self.top_margin
                y1 = self.top_margin
            elif self.pos == 'center':
                y0 = self.bipolar_offset
                y1 = self.bipolar_offset
            elif self.pos == 'bottom':
                y0 = self.bottom_margin
                y1 = self.bottom_margin

        chart.create_line(x0,y0, x1,y1, fill=self.color)
        self.place_ticks(chart, x0,y0, x1,y1)

        text = '{}'.format(self.units)
        if self.range.tmax.exponent != 0:
            text += '(E{:+})'.format(self.range.tmax.exponent)

        if self.axis == 'x':
            x = x1
            y = y0 + 20
            anchor = tk.CENTER
        else:
            x = x1 + 10
            y = y0 + 10
            anchor = tk.SW
            
        chart.create_text(x, y, anchor=anchor, text=text,
                          fill=self.color)
            
        return

    def place_ticks(self, chart, x0,y0, x1,y1):
        print('placing ticks({}): {}'.format(self.axis, self.range))
        index = -1
        for tick in self.range.ticks():
            print(' tick {}'.format(tick))
            index += 1
            label = str(tick.coefficient)
            pos = self.to_chart(chart, tick.value)
            if self.axis == 'x':
                if index == 0:
                    continue
                
                chart.create_line(pos,y0, pos,y1+5, fill= self.color)
                if index % 2:
                    continue
                
                chart.create_text(pos, y0-10, anchor=tk.CENTER,
                                  text=label, fill=self.color)
            else:
                chart.create_line(x0,pos, x1+5,pos, fill= self.color)
                if index % 2:
                    continue
                
                chart.create_text(x0-5, pos+10, anchor=tk.SE,
                                  text=label, fill=self.color)
        return
    
    def to_chart(self, chart, value):
        if value < self.range.tmin.value:
            raise ValueError('{}: {}<{}'.format(self.axis, value, self.range.tmin.value))
        if value > self.range.tmax.value:
            raise ValueError('{}: {}>{}'.format(self.axis, value, self.range.tmax.value))
        
        if self.axis == 'y':
            val = self.length * (value/self.range.spread)
            val += self.bipolar_offset
            val = chart.height - val
        else:
            # x-axis value (time)
            val = self.length * (value/self.range.spread) + self.left_margin
        
        return val

class LinearScale(Scale):
    def __init__(self, axis, position='left', units='', color='black'):
        super().__init__(axis, position, units, color)
        return
