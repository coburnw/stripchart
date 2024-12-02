class Axis():
    __index = None
    
    def __init__(self, axis, title, color):
        if axis not in ['x', 'y', 'zy']:
            raise ValueError
        
        self.axis = axis
        self.title = title
        self.color = color
        return

class HorizontalAxis(Axis):
    __index = 0
    
    def __init__(self, title='', color='black'):
        super().__init__('x', title, color)
        self._index = self.get_next_index()
        
        return

    @classmethod
    def get_next_index(cls):
        cls.__index += 1
        return cls.__index

    @property
    def index(self):
        return self._index
    
class VerticalAxis(Axis):
    __index = 0
    def __init__(self, title='', bipolar=False, color='black'):
        super().__init__('y', title, color)
        self.bipolar = bipolar
        self._index = self._get_next_index()
        return

    @classmethod
    def _get_next_index(cls):
        cls.__index += 1
        return cls.__index

    @property
    def index(self):
        return self._index
    
    @property
    def height(self):
        return self.length

    
