#Python version 3.9.4
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

# Step 1: Load and preprocess the data
data_dir = "/Users/parshvamehta/Desktop/MLProject/Data"
image_height, image_width = 128, 128 
num_channels = 3

# List all files in the data directory
file_names = os.listdir(data_dir)

print(file_names)
# Initialize lists to store images and labels
images = []
labels = []

# Loop through each file in the directory
for file_name in file_names:
    # Extract the label from the file name (assuming the file name contains the label information)
    if 'tumor' in file_name.lower():
        label = 1  # 1 for tumor
    else:
        label = 0  # 0 for no tumor

    # Load the image using OpenCV (or PIL)
    image_path = os.path.join(data_dir, file_name)
    image = cv2.imread(image_path)  # Or Image.open(image_path)
    
    # Resize the image to the desired dimensions and append it to the list
    image = cv2.resize(image, (image_height, image_width))  # Or image.resize((image_height, image_width))
    images.append(image)
    labels.append(label)

# Convert the lists to numpy arrays
X = np.array(images)
y = np.array(labels)

# Split the data into training, validation, and test sets (e.g., 70%, 15%, 15%)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Print the shape of the data arrays to ensure everything is correct
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_val shape:", X_val.shape)
print("y_val shape:", y_val.shape)
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

# Step 2: Preprocess the data
# Normalize pixel values to the range [0, 1]
X_train = X_train / 255.0
X_val = X_val / 255.0
X_test = X_test / 255.0

# Step 3: Create the CNN model
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_height, image_width, num_channels)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Binary classification (tumor or no tumor)
])

# Step 4: Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 5: Train the model
epochs = 10
batch_size = 32
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_val, y_val))

# Step 6: Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_accuracy}')

# Step 7: Visualize the training process
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
