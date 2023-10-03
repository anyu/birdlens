import os
import time

def check_for_new_images(directory_to_monitor, ml_model_path, image_extensions=(".jpg", ".jpeg", ".png"), check_interval=10):
  new_image_files = []
  prev_files = set()

  while True:
    current_files = set(os.listdir(directory_to_monitor))
    new_files = current_files - prev_files

    for file in new_files:
      if file.lower().endswith(image_extensions):
        new_image_files.append(file)
    prev_files = current_files
    time.sleep(check_interval)
    return new_image_files

def classify_bird(image_file):
  image_path = os.path.join(directory_to_watch, image_file)
  # TODO: Use fast.ai or pytorch to classify image
    # img = open_image(image_path)
    # prediction = learn.predict(img)

    # print(f"Image: {image_file}, Predicted Class: {prediction[0]}, Confidence: {prediction[2][prediction[1]].item():.4f}")

def main():
  directory_to_monitor = "/path/to/your/directory"
  new_images = check_for_new_images(directory_to_monitor, ml_model_path)
  ml_model_path = "/path/to/ml/model.pkl"

  if new_images:
    print("New image files detected:")
    for image in new_images:
      classify_bird(image)
  else:
    print("No new image files detected.")

if __name__ == "__main__":
  main()