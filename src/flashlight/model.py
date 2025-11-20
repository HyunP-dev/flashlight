from io import BytesIO
from PIL import Image
from transformers import pipeline


def is_nsfw(raw) -> bool:
    img = Image.open(BytesIO(raw))
    classifier = pipeline(
        "image-classification", model="Falconsai/nsfw_image_detection"
    )
    for e in classifier(img):
        if e["label"] == "nsfw":
            if e["score"] > 0.8:
                return True
    return False
