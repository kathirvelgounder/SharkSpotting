
#class used to provide a common structure 
class Label:
    def __init__(self, group, x_min, x_max, y_min, y_max):
        self.group = group
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
