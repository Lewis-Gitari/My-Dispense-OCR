from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np
import re

# Update the path according to your Tesseract installation location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.filter(ImageFilter.MedianFilter())
    img = np.array(img)
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    temp_filename = 'temp_image.png'
    cv2.imwrite(temp_filename, img)
    return temp_filename

def extract_text_from_image(image_path):
    preprocessed_image_path = preprocess_image(image_path)
    extracted_text = pytesseract.image_to_string(preprocessed_image_path)
    return extracted_text

drug_names = ["Aspirin", "Paracetamol", "Ibuprofen", "Metformin", "Amoxicillin"]

def filter_drug_names(text, drug_list):
    words = re.findall(r'\b\w+\b', text)
    found_drugs = [word for word in words if word.capitalize() in drug_list]
    return found_drugs

if __name__ == "__main__":
    image_path = 'data/prescription2.jpeg'
    extracted_text = extract_text_from_image(image_path)
    found_drugs = filter_drug_names(extracted_text, drug_names)
    print("Extracted Text:", extracted_text)
    print("Detected Drugs:", found_drugs)
