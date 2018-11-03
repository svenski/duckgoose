import os
from duckgoose import fetchImagesAndPrepForClassification

# dictionary structure `class_name => search term`
user = os.environ['USER']
image_classes = { 'ducks' : 'ducks -rubber' , 'geese' : 'geese' }
download_path = f'/home/{user}/data/dev/downloaded_from_google'
output_path = f'/home/{user}/data/dev/ducksgeese/'
number_of_images = 30

fetchImagesAndPrepForClassification(image_classes, download_path, output_path, number_of_images, download_if_paths_exists=False)

