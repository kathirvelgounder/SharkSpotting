#Use these so we can substitute out PyTorch and Tensorflow models interchangeably when we want to make predictions.
#Python has weird support for interfaces, and I don't expect us to have any other models besides these two,
#so make sure they have 
import Label

class PyTorchModel:
    def __init__(self, model):
        pass
    
    #Make a prediction on an image and return a list of Label objects
    def predict(frame) -> List[Label]:
        pass



class TFModel:
    def __init__(self, model):
        pass

    #Make a prediction on an image and return a list of Label objects
    def predict(frame) -> List[Label]:
        pass
