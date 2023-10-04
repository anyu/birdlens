import os
import time
import torch
# from fastcore.all import *
# from fastai.vision import *
from fastai.vision.all import * 

RPI_CAM_CAPTURES_PATH = "./camera_captures"
ML_MODEL_PATH = "./birdlens_resnet_34_model.pkl"

def check_for_new_images(directory_to_monitor, ml_model_path, prev_files):
  current_files = set(os.listdir(directory_to_monitor))
  new_files = current_files - prev_files

  prev_files = current_files
  return new_files

def classify_bird(image_file):
  image_path = os.path.join(RPI_CAM_CAPTURES_PATH, image_file)
  img = open_image(image_path)
  learner = load_learner(ML_MODEL_PATH, cpu=False)
  prediction = learner.predict(img)

  print(f"Image: {image_file}, Predicted Class: {prediction[0]}, Confidence: {prediction[2][prediction[1]].item():.4f}")

def main():
  prev_files = set()
  print("test")
  while True:
    new_images = check_for_new_images(RPI_CAM_CAPTURES_PATH, ML_MODEL_PATH, prev_files)

    if new_images:
      print("New image files detected:")
      for image in new_images:
        classify_bird(image)
    else:
      print("No new image files detected.")
    
    time.sleep(10)  

if __name__ == "__main__":
  main()