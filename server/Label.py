
#class used to provide a common structure 
#use "id" as a numerical identifier for every object present in the frame
class Label:
    def __init__(self, id: int, group: str, x_min: int, x_max: int, y_min: int, y_max: int, color: str, score: float):
        self.group = group
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.color = color
        self.score = score

    def get_midpoint(self):
        return (int)((self.x_max-self.x_min)/2, (self.y_max-self.y_min)/2)

    def __repr__(self):
        return "Label({}, {}, {}, {}, {}, {})".format(self.id, self.group, self.x_min, self.x_max, self.y_min, self.y_max)
