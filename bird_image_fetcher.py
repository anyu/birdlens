import flickrapi
import os
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

BIRD_LIST_FILE = "us_northeast_feeder_birds.txt"
BIRD_IMAGES_DIR = 'bird_images'
FLICKR_DEFAULT_PHOTO_URL_TEMPLATE = "https://farm{}.staticflickr.com/{}/{}_{}.jpg"

flickr = flickrapi.FlickrAPI(
  config["FLICKR_API_KEY"], 
  config["FLICKR_API_SECRET"]
)

def main():
  try:
    with open(BIRD_LIST_FILE, "r") as f:
      bird_names = f.read().splitlines()
    
    for bird_name in bird_names:
      search_flickr_for_bird(bird_name, 1)
      print(f"Searching for {bird_name} on Flickr...")

  except FileNotFoundError:
    print(f"File not found: {BIRD_LIST_FILE}") 
  except Exception as e:
    print(f"An error occurred: {str(e)}")

def search_flickr_for_bird(bird_name, max=10):
  try:
    photos = flickr.walk(
      text=bird_name, # or use tags with tag_mode='all',
      per_page=1,
      privacy_filters = 1, # only public photos
      sort = 'relevance',
      media='photos', 
      extras='url_c') # medium size, 800px pics

    for i, photo in enumerate(photos):
      if i >= max:
        break
      photo_url = photo.get('url_c') or FLICKR_DEFAULT_PHOTO_URL_TEMPLATE.format(
          photo.get('farm', ''), photo.get('server', ''), photo.get('id', ''), photo.get('secret', '')
        )

      print(f"Found {bird_name} photo {photo_url}")

      # Make folders for each type of bird
      BIRD_NAME_DIR = os.path.join(BIRD_IMAGES_DIR, bird_name)
      if not os.path.exists(BIRD_IMAGES_DIR):
        os.makedirs(BIRD_IMAGES_DIR)

      if not os.path.exists(BIRD_NAME_DIR):
        os.makedirs(BIRD_NAME_DIR)

      photo_id = photo.get('id')
      filepath = os.path.join(BIRD_NAME_DIR, f'{bird_name}_{photo_id}.jpg')

      response = requests.get(photo_url)
      if response.status_code == 200:
          with open(filepath, 'wb') as f:
            f.write(response.content)
          print(f"Downloaded {filepath}")

  except flickrapi.exceptions.FlickrError as e:
    print(f"Error searching for {bird_name}: {str(e)}")

if __name__ == "__main__":
  main()