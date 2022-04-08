from turtle import forward
from torch import nn
import torch
from torchvision import models

NUM_CLASSES = 131

class DetectionClassificationModel():
    def __init__(self, w_cl_path, num_classes=NUM_CLASSES):
        detec_model = models.detection.fasterrcnn_mobilenet_v3_large_fpn(pretrained=True)
        detec_model.eval()

        class_model = models.densenet121(pretrained=True)
        class_model.classifier = nn.Linear(in_features=class_model.classifier.in_features, out_features=num_classes, bias=True)
        class_model.load_state_dict(torch.load(w_cl_path, map_location='cpu'))
        class_model.eval()

        
    def forward(x):
        pass