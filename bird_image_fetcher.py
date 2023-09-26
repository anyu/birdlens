import flickrapi
import os
import requests
from dotenv import dotenv_values

secrets = dotenv_values(".env")

bird_list_file = "us_northeast_feeder_birds.txt"

flickr = flickrapi.FlickrAPI(secrets["FLICKR_API_KEY"], secrets["FLICKR_API_SECRET"])

def main():
  try:
    with open(bird_list_file, "r") as f:
      bird_names = f.read().splitlines()
    
    for bird_name in bird_names:
      search_flickr_for_bird(bird_name)
      print(f"Searching for {bird_name} on Flickr...")

  except FileNotFoundError:
    print(f"File not found: {bird_list_file}") 
  except Exception as e:
    print(f"An error occurred: {str(e)}")

def search_flickr_for_bird(bird_name):
  try:
    photos = flickr.walk(
      text=bird_name, # or use tags with tag_mode='all',
      per_page=1,
      privacy_filters = 1, # only public photos
      sort = 'relevance',
      media='photos', 
      extras='url_c') # medium size, 800px pics

    for i, photo in enumerate(photos):
      if i >= 10:
        break # Stop after 10 photos per bird
      photo_url = photo.get('url_c')
      if photo_url is None: # Is this a possible case?
        photo_url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(
          photo.get('farm', ''), photo.get('server', ''), photo.get('id', ''), photo.get('secret', '')
        )
      print(f"Found {bird_name} photo {photo_url}")

      bird_images_dir = 'bird_images'
      bird_name_dir = os.path.join('bird_images', bird_name)

      if not os.path.exists(bird_images_dir):
        os.makedirs(bird_images_dir)

      if not os.path.exists(bird_name_dir):
        os.makedirs(bird_name_dir)

      photo_id = photo.get('id')
      filepath = os.path.join(bird_name_dir, f'{bird_name}_{photo_id}.jpg')

      response = requests.get(photo_url)
      if response.status_code == 200:
          with open(filepath, 'wb') as f:
            f.write(response.content)
          print(f"Downloaded {filepath}")

  except flickrapi.exceptions.FlickrError as e:
    print(f"Error searching for {bird_name}: {str(e)}")

if __name__ == "__main__":
  main()