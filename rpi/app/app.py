import os
import time
import torch
import numpy as np
from fastcore.all import *
from fastai.vision import * 
from fastai.vision.all import *

print("Script is running...")

RPI_CAM_CAPTURES_PATH = "./camera_captures"
GLOBAL_FILELIST_PATH = "./global_filelist.txt"
CLASSIFIED_IMAGES_PATH = "./classified_images"
ML_MODEL_PATH = "./birdlens_resnet_34_model.pkl"

def check_for_new_images(directory_to_monitor, ml_model_path, prev_images):
  with open(GLOBAL_FILELIST_PATH, 'r') as file:
    prev_images = [line.strip() for line in file]
    print("Previously classified images:", prev_images)

  current_files = set(os.listdir(directory_to_monitor))
  new_files = current_files - set(prev_images)
  return new_files

def classify_bird(image_file):
  image_path = os.path.join(RPI_CAM_CAPTURES_PATH, image_file)
  img = Image.open(image_path)
  imgArr = np.asarray(img)
  learner = load_learner(ML_MODEL_PATH, cpu=True)

  prediction = learner.predict(imgArr)
  print(f"Image: {image_file}, Predicted Class: {prediction[0]}, Confidence: {prediction[2][prediction[1]].item():.4f}")

def update_global_filelist(new_file):
  print(f"Updating global filelist with new file {new_file}")
  with open(GLOBAL_FILELIST_PATH, 'a') as file:
    file.write(new_file + '\n')

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

def main():
  prev_files = set()
  while True:
    new_images = check_for_new_images(RPI_CAM_CAPTURES_PATH, ML_MODEL_PATH, prev_files)

    if new_images:
      print("New images detected:")
      for image in new_images:
        classify_bird(image)
        update_global_filelist(image)
        move_file(image)
    else:
      print("No new images detected.\n")
    
    time.sleep(10)  

if __name__ == "__main__":
	main()
 

