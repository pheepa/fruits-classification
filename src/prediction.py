from io import BytesIO
from PIL import Image
import torch
from torchvision.models import mobilenet_v2
from torchvision import transforms

PATH = "models/mobilenet_2ep.pkl"
TARGET_MAP = {
    'apple_season': 0,
    'lemon': 1,
    'persimmon': 2,
    'qiwi': 3,
    'tomato': 4
}
CLASSES = ['apple_season', 'lemon', 'persimmon', 'qiwi', 'tomato']
TRANSFROM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean = [ 0.485, 0.456, 0.406 ],
                         std  = [ 0.229, 0.224, 0.225 ]),
    ])
model = None


def load_model():
    
    model = mobilenet_v2(pretrained=True)
    model.classifier[1] = torch.nn.Linear(1280, len(TARGET_MAP), bias=True)
    model.classifier = torch.nn.Sequential(
        *model.classifier,
        torch.nn.Softmax(),
    )
    model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))
    model.eval()

    return model


def predict(image: Image.Image):
    global model
    if model is None:
        model = load_model()

    image_pr = TRANSFROM(image)
    image_pr = image_pr[None, :]
    with torch.no_grad():
        pred = model(image_pr).detach().numpy()
    cl = int(pred.argmax(1)[0])
    response = {'class': cl, 'class_name': CLASSES[cl]}

    return response


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

