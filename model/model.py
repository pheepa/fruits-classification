from torch import nn
from torchvision import models


densenet121_0 = models.densenet121(pretrained=True)
densenet121_0.classifier = nn.Linear(in_features=densenet121_0.classifier.in_features, out_features=len(training.classes), bias=True)