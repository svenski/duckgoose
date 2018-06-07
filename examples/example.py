from duckgoose import fetchImagesAndPrepForClassification

# dictionary structure `class_name => search term`
image_classes = { 'ducks' : 'ducks -rubber' , 'geese' : 'geese' }
download_path = '/home/myuser/data/downloaded_from_google'
output_path = '/home/myuser/data/ducksgeese/'
number_of_images = 100

fetchImagesAndPrepForClassification(image_classes, download_path, output_path, number_of_images)

