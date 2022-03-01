from torch import nn
from torchvision import models

num_classes = 131

def get_model(num_classes=num_classes):
    densenet121_0 = models.densenet121(pretrained=True)
    densenet121_0.classifier = nn.Linear(in_features=densenet121_0.classifier.in_features, out_features=num_classes, bias=True)
    return densenet121_0