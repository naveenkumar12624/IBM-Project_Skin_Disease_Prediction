
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
import os
import numpy as np
from tensorflow import keras

app = Flask(__name__)


# Set the path to the model
model_path = "/home/jovyan/SkinDiseasePredictor/your_model.h5"  # Update with your model file

# Function to classify an uploaded image
def classify_image(image_path):
    model = keras.models.load_model(model_path)
    user_input_image = keras.preprocessing.image.load_img(image_path, target_size=image_size)
    user_input_image = keras.preprocessing.image.img_to_array(user_input_image) / 255.0
    user_input_image = np.expand_dims(user_input_image, axis=0)
    
    # Make a prediction
    prediction = model.predict(user_input_image)
    class_index = np.argmax(prediction)
    
    # Extract the class labels from class_indices
    class_labels = list(train_generator.class_indices.keys())
    
    # Access the predicted class label
    disease_label = class_labels[class_index]
    
    # Calculate the accuracy as a percentage
    accuracy_percentage = prediction[0][class_index] * 100
    
    # Display the predicted disease, accuracy, and other disease probabilities
    print(f"The predicted disease may be {disease_label}")
    print(f"By the User Given Image,the Prediction Accuracy is: {accuracy_percentage:.2f}%\n")
    
    # Display the probabilities of other diseases
    for i, label in enumerate(class_labels):
        probability = prediction[0][i] * 100
        print(f"Also the Probability of {label}: {probability:.2f}%")

@app.route("/", methods=["GET", "POST"])
def upload_image():
    form = UploadForm()

    if form.validate_on_submit():
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = form.file.data

        # Check if the file name is empty
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file:
            filename = os.path.join("uploads", file.filename)
            file.save(filename)

            # Perform image classification
            result = classify_image(filename)
            return render_template("/home/jovyan/SkinDiseasePredictor/result.html", result=result)

    return render_template("/home/jovyan/SkinDiseasePredictor/upload.html")

if __name__ == "__main__":
    app.run(debug=True)







