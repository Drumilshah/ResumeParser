from html import entities
import spacy, pickle, os, pytesseract
from PIL import Image

def inference():
    model = None
    if(not model):
        path = "/Users/drumilshah/Documents/ResumeParser/finalized_model.sav"
        model = pickle.load(open(path, 'rb'))
    
    text = ""
    for root, dirs, files in os.walk('./temp'):
        for file in files:
            path = os.path.join(root, file)
            img = Image.open(path)
            text += pytesseract.image_to_string(img)
            os.remove(path)
    os.rmdir('./temp')
    result = model(text)
    labels = set([w.label_ for w in result.ents])
    d = {}
    for label in labels:
        entities = [e.text for e in result.ents if e.label_ == label]
        entities = list(set(entities))
        d[label] = entities
    print(d)
    return d