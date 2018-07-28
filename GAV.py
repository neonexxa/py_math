
# coding: utf-8

# In[10]:


import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'resources/wakeupcat.jpg')

# Loads the image into memory
with io.open('/Users/neonexxa/Downloads/puppy-090517-dog-featured-355w-200h-d.jpeg', 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels: {}'.format(labels[0].description))
# for label in labels:
#     print(label.description)


# In[ ]:




