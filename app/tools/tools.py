from torchvision import transforms
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
IMAGE_SIZE = [100]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_img(img):
    img = Image.open(img).convert('RGB')
    transformer = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.6840562224388123, 0.5786514282226562, 0.5037682056427002],
                             [0.3034113645553589, 0.35993242263793945, 0.39139702916145325])
        ])
    return transformer(img)
    