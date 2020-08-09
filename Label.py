
#class used to provide a common structure 
#use "id" as a numerical identifier for every object present in the frame
class Label:
    def __init__(self, id, group, x_min, x_max, y_min, y_max):
        self.group = group
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def get_midpoint():
        return (int)((self.x_max-self.x_min)/2, (self.y_max-self.y_min)/2)
