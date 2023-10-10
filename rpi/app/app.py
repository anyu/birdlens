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
CLASSIFIED_IMAGES_PATH = "./classified_images"
UNKNOWN_IMAGES_PATH = "./unknown_images"

ML_MODEL_PATH = "./birdlens_resnet_34_model.pkl"
CONFIDENCE_THRESHOLD = 0.5

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
  def move_file(file, destination_directory):
    if not os.path.exists(destination_directory):
      print(f"{destination_directory} does not exist. Creating...")
      os.makedirs(destination_directory)

    source_path = os.path.join(RPI_CAM_CAPTURES_PATH, file)
    destination_path = os.path.join(destination_directory, file)

    try:
      os.rename(source_path, destination_path)
      print(f"Moved {file} to {destination_directory}\n")
    except Exception as e:
      print(f"Error moving {file}: {str(e)}")

class ImageProcessor:
  def __init__(self, classifier, file_handler, email_sender):
    self.classifier = classifier
    self.file_handler = file_handler
    self.email_sender = email_sender

  def process_images(self, prev_images):
    new_files = set(os.listdir(RPI_CAM_CAPTURES_PATH)) - set(prev_images)
    if new_files:
      print("New images found.")
      for image_file in new_files:
        prediction_result = self.classifier.classify_image(image_file)
        prediction_class = prediction_result[0]
        confidence = prediction_result[2][prediction_result[1]].item()

        base_image_name = os.path.basename(image_file)
        print(f"Image: {base_image_name}, Predicted Class: {prediction_class}, Confidence: {confidence:.4f}")
        if confidence > CONFIDENCE_THRESHOLD:
          print("Pretty confident!")
          source_path = os.path.join(RPI_CAM_CAPTURES_PATH, image_file)
          self.trigger_email(prediction_class, confidence, source_path)
          self.file_handler.move_file(image_file, CLASSIFIED_IMAGES_PATH)
        else:
          print("Not confident. Please manually classify.")
          self.file_handler.move_file(image_file, UNKNOWN_IMAGES_PATH)

    else:
      print("No new images found.")

  def trigger_email(self, prediction_class, confidence, image_file):
    base_image_name = os.path.basename(image_file)

    subject = '[birdlens] Bird detected!'
    message_body = f'birdlens detected this bird:\n\n'
    message_body += f"Image: {base_image_name}\n"
    message_body += f"Predicted Class: {prediction_class}\n"
    message_body += f"Confidence: {confidence:.4f}"

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