import os
import time
import torch
import numpy as np
from fastcore.all import *
from fastai.vision import * 
from fastai.vision.all import *
from dotenv import load_dotenv
from custom_email_sender import EmailSender

load_dotenv()
print("Script is running...")

RPI_CAM_CAPTURES_PATH = "./camera_captures"
GLOBAL_FILELIST_PATH = "./global_filelist.txt"
CLASSIFIED_IMAGES_PATH = "./classified_images"
ML_MODEL_PATH = "./birdlens_resnet_34_model.pkl"

class ImageClassifier:
  def __init__(self, model_path):
    self.model_path = model_path
    self.learner = load_learner(model_path, cpu=True)

  def classify_image(self, image_file):
    image_path = os.path.join(RPI_CAM_CAPTURES_PATH, image_file)
    img = Image.open(image_path)
    img_arr = np.asarray(img)
    prediction = self.learner.predict(img_arr)
    return prediction

class FileHandler:
  @staticmethod
  def update_global_filelist(new_file):
    print(f"Updating global filelist with new file {new_file}")
    with open(GLOBAL_FILELIST_PATH, 'a') as file:
      file.write(new_file + '\n')

  @staticmethod
  def move_file(file):
    if not os.path.exists(CLASSIFIED_IMAGES_PATH):
      print(f"{CLASSIFIED_IMAGES_PATH} does not exist. Creating...")
      os.makedirs(CLASSIFIED_IMAGES_PATH)

    source_path = os.path.join(RPI_CAM_CAPTURES_PATH, file)
    destination_path = os.path.join(CLASSIFIED_IMAGES_PATH, file)

    try:
      os.rename(source_path, destination_path)
      print(f"Moved {file} to {CLASSIFIED_IMAGES_PATH}\n")
    except Exception as e:
      print(f"Error moving {file}: {str(e)}")

class ImageProcessor:
  def __init__(self, classifier, file_handler, email_sender):
    self.classifier = classifier
    self.file_handler = file_handler
    self.email_sender = email_sender

  def process_images(self, prev_images):
    new_files = set(os.listdir(RPI_CAM_CAPTURES_PATH)) - set(prev_images)
    for image_file in new_files:
      prediction_result = self.classifier.classify_image(image_file)
      source_path = os.path.join(RPI_CAM_CAPTURES_PATH, image_file)

      self.trigger_email(prediction_result, source_path)
      self.file_handler.update_global_filelist(image_file)
      self.file_handler.move_file(image_file)

  def trigger_email(self, prediction_result, image_file):
    print(f"Image: {image_file}, Predicted Class: {prediction_result[0]}, Confidence: {prediction_result[2][prediction_result[1]].item():.4f}")
    subject = 'Bird detected!'
    message_body = 'birdlens detected this bird:'

    self.email_sender.send_email(subject, message_body, image_file)

def main():
  sender_email = os.getenv('SENDER_EMAIL')
  sender_password = os.getenv('SENDER_PASSWORD')
  recipient_email = os.getenv('RECIPIENT_EMAIL')

  if not sender_email or not sender_password or not recipient_email:
    print("Error: Missing required environment variables.")
    exit(1)

  email_sender = EmailSender(sender_email, sender_password, recipient_email)
  file_handler = FileHandler()
  image_classifier = ImageClassifier(ML_MODEL_PATH)
  image_processor = ImageProcessor(image_classifier, file_handler, email_sender)

  prev_files = set()
  while True:
    image_processor.process_images(prev_files)
    time.sleep(10)  

if __name__ == "__main__":
  main()