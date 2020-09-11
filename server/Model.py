#Use these so we can substitute out PyTorch and Tensorflow models interchangeably when we want to make predictions.
#Python has weird support for interfaces, and I don't expect us to have any other models besides these two,
#so make sure they have 
import sys
print(sys.path)
from Label import Label
from typing import List
import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.faster_rcnn import FasterRCNN
import torchvision.models.detection.faster_rcnn
from torchvision.models.detection.rpn import AnchorGenerator, RegionProposalNetwork, RPNHead
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone
from torchvision.models.detection.transform import GeneralizedRCNNTransform
from torchvision.models.detection.roi_heads import RoIHeads
import cv2
import json
from labelbox import Client
import urllib.request
from urllib.parse import urlparse
import io
from PIL import Image
import PIL
import requests
import os
from os import path
import time
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import numpy as np
import sys
import scipy
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#contains info about each class, i.e. what color sharks bounding box should be
with open("classes.json") as json_file:
    classes = json.load(json_file)

class PyTorchModel:

    #create model by loading it in from Google Drive path
    def __init__(self, f):
        trainable_backbone_layers = 5
        pretrained = True
        backbone = resnet_fpn_backbone('resnet50', True, trainable_layers=trainable_backbone_layers)
        self.model = FasterRCNN(backbone, num_classes=10, max_size = 3840, min_size = 2160, rpn_pre_nms_top_n_train=2000, rpn_pre_nms_top_n_test=2000, rpn_post_nms_top_n_train=2000, rpn_post_nms_top_n_test=2000, box_detections_per_img=100,rpn_nms_thresh=0.01, box_nms_thresh=0.01)

        #num_classes = 10
        #self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        #in_features = self.model.roi_heads.box_predictor.cls_score.in_features
        #self.model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(device)
        if (isinstance(f, str)): #local file
            print("Loading model from local file at {}".format(f))
            self.model.load_state_dict(torch.load(f, map_location=device))
        elif (isinstance(f, io.BytesIO)): #stream
            print("Loading model from stream")
            pass
        
    def predict(self, image) -> List[Label]:
        frame = torchvision.transforms.ToTensor()(image)
        frame = frame[None, :, :]
        self.model.eval()
        prediction = self.model(frame)
        print(prediction)
        boxes = prediction[0]["boxes"]
        labels = prediction[0]["labels"]
        scores = prediction[0]["scores"]
        ret = list()
        for i in range(0, len(boxes)):
            score: float = float(scores[i].item())
            xmin: int = int(boxes[i][0].item())
            ymin: int = int(boxes[i][1].item())
            xmax: int = int(boxes[i][2].item())
            ymax: int = int(boxes[i][3].item())
            group: str = classes[str(labels[i].item())]["category"]
            color: str = classes[str(labels[i].item())]["color"]
            ret.append(Label(i, group, xmin, xmax, ymin, ymax, color, score))
        return ret


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
