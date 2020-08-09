#Use these so we can substitute out PyTorch and Tensorflow models interchangeably when we want to make predictions.
#Python has weird support for interfaces, and I don't expect us to have any other models besides these two,
#so make sure they have 
from Label import Label
from typing import List

class PyTorchModel:
    def __init__(self, model):
        pass
    
    #Make a prediction on an image and return a list of Label objects
    def predict(frame) -> List[Label]:
        #proof of concept, use actual model.
        labels = list()
        labels.append(Label(1, "shark", 20, 150, 20, 150))
        labels.append(Label(2, "person", 200, 500, 200, 500))
        return labels



class TFModel:
    def __init__(self, model):
        pass

    #Make a prediction on an image and return a list of Label objects
    def predict(frame) -> List[Label]:
        #proof of concept, use actual model.
        labels = list()
        labels.append(Label(1, "shark", 20, 150, 20, 150))
        labels.append(Label(2, "person", 200, 500, 200, 500))
        return labels
