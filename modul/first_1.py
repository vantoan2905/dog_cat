
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd 
import numpy as np

import warnings
warnings.filterwarnings('ignore')

from tensorflow import keras
from keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout,Flatten,Dense
from tensorflow.keras.layers import Conv2D, MaxPool2D
from tensorflow.keras.utils  import image_dataset_from_directory 
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras .preprocessing import image_dataset_from_directory 

import os
import matplotlib.image as mping

path = os.path.join("D:\\learn\\python\\learn_ml\\dog_cat\\input\\train_frames\\train")

classes = os.listdir(path=path)
print(classes)

fig = plt.gcf()
fig.set_size_inches(16, 16)
cat_dir = os.path.join(r'D:\\learn\\python\\learn_ml\\dog_cat\\input\\train_frames\\train\\cat')
dog_dir = os.path.join(r'D:\\learn\\python\\learn_ml\\dog_cat\\input\\train_frames\\train\\dog')

cat_names = os.listdir(cat_dir)
dog_names = os.listdir(dog_dir)
# print(cat_names)
# print(dog_names)
pic_index = 210
cat_images = []
dog_images = []

# cat_images = [os.path.join(cat_dir, fname) for fname in os.listdir(cat_dir)[:8]]
# dog_images = [os.path.join(dog_dir, fname) for fname in os.listdir(dog_dir)[:8]]
        
# print(cat_images)
# print(dog_images)
# for i, img_path in enumerate(cat_images + dog_images):
#     plt.subplot(4, 4, i + 1)
#     plt.axis('off')
#     img = mping.imread(img_path)
#     plt.imshow(img)

# plt.show()

base_dir = path

# Create datasets 
train_datagen = image_dataset_from_directory(base_dir, 
												image_size=(200,200), 
												subset='training', 
												seed = 1, 
												validation_split=0.1, 
												batch_size= 32) 
test_datagen = image_dataset_from_directory(base_dir, 
												image_size=(200,200), 
												subset='validation', 
												seed = 1, 
												validation_split=0.1, 
												batch_size= 32)


model = tf.keras.models.Sequential([ 
	layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)), 
	layers.MaxPooling2D(2, 2), 
	layers.Conv2D(64, (3, 3), activation='relu'), 
	layers.MaxPooling2D(2, 2), 
	layers.Conv2D(64, (3, 3), activation='relu'), 
	layers.MaxPooling2D(2, 2), 
	layers.Conv2D(64, (3, 3), activation='relu'), 
	layers.MaxPooling2D(2, 2), 

	layers.Flatten(), 
	layers.Dense(512, activation='relu'), 
	layers.BatchNormalization(), 
	layers.Dense(512, activation='relu'), 
	layers.Dropout(0.1), 
	layers.BatchNormalization(), 
	layers.Dense(512, activation='relu'), 
	layers.Dropout(0.2), 
	layers.BatchNormalization(), 
	layers.Dense(1, activation='sigmoid') 
]) 

model.summary()

keras.utils.plot_model( 
	model, 
	show_shapes=True, 
	show_dtype=True, 
	show_layer_activations=True
) 
model.compile( 
	loss='binary_crossentropy', 
	optimizer='adam', 
	metrics=['accuracy'] 
) 
history = model.fit(train_datagen, 
          epochs=10, 
          validation_data=test_datagen) 

history_df = pd.DataFrame(history.history) 
history_df.loc[:, ['loss', 'val_loss']].plot() 
history_df.loc[:, ['accuracy', 'val_accuracy']].plot() 
plt.show() 


from tensorflow.keras.preprocessing import image 

#Input image 
test_image = image.load_img(r'D:\learn\python\learn_ml\dog_cat\input\train_frames\train\cat\cat003.png',target_size=(200,200)) 

#For show image 
plt.imshow(test_image) 
test_image = image.img_to_array(test_image) 
test_image = np.expand_dims(test_image,axis=0) 

# Result array 
result = model.predict(test_image) 

#Mapping result array with the main name list 
i=0
if(result>=0.5): 
    print("Dog") 
else: 
    print("Cat")
