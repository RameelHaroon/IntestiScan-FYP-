from django.shortcuts import render, redirect
from .models import User
from .models import Image as ImageModel
from .form import UserSignUpForm, UserSignInForm, ImageForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppresses INFO and WARNING messages from TensorFlow
import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras.preprocessing import image
#from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from datetime import date
#from keras_preprocessing.image import load_img, img_to_array


# Get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the trained model
model_path = os.path.join(BASE_DIR, 'FypApp', 'model', 'ResNet.h5')
model = tf.keras.models.load_model(model_path)



# temporay solution
from keras._tf_keras.keras.applications.resnet50 import preprocess_input
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array, array_to_img
from PIL import Image


def classify_image(image_path):

    result = {0: 'dyed-lifted-polyps',
            1: 'dyed-resection-margins',
            2: 'esonphagitis',
            3: 'normal-cecum',
            4: 'normal-pylorus',
            5: 'normal-z-line',
            6: 'polyps',
            7: 'ulcerative-colitis'}
    # Load the image and resize it to match the model's input shape
    img = Image.open(image_path)
    img = img.resize((224, 224))
    # Convert the image to a numpy array
    img_array = img_to_array(img)
    # Expand the dimensions to create a batch of size 1
    img_array = np.expand_dims(img_array, axis=0)
    # Preprocess the input according to the requirements of the model
    img_array = preprocess_input(img_array)
    # Make predictions
    predictions = model.predict(img_array)
    # Get the predicted class label
    class_label = np.argmax(predictions, axis=1)
    return result[class_label[0]]

def image_upload_view(request, user_id):

    user_instance = User.objects.get(id=user_id)  # Fetch the User instance

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.user_id = user_id
            image_instance.date = date.today()
            image_instance.save()  # Save the instance to generate the path
            image_path = image_instance.image.path
            print(f"Image path: {image_path}")  # Debugging line to check the file path

            if os.path.exists(image_path):
                classification_result = classify_image(image_path)
                image_instance.type = classification_result
                image_instance.save()
                return redirect("dashboard")
            else:
                print("File not found:", image_path)
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})

def delete_image(request, image_id):
    DeleteMember = ImageModel.objects.get(id=image_id)
    DeleteMember.delete()
    return redirect("dashboard")

# Old Code
def Main(request):
    return render(request, 'index.html' )

def dasboard(request):


    if not request.session.get('user_loggedin'):
        return redirect('SignIn')  # Redirect to sign-in if the user is not logged in

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('SignIn')
    
    print(user_id)
    user_data = User.objects.get(id=user_id)
    user_images = ImageModel.objects.filter(user_id=user_id)  # Fetch images associated with the user
    return render(request, 'dashboard.html', {'user': user_data, 'images': user_images})

def SignIn(request, ):
    
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)  # Fetch user by provided email
            except User.DoesNotExist:
                form.add_error(None, "Invalid email.")
            else:
                if password == user.password:
                    # Password is correct
                    request.session['user_id'] = user.id  # Create session
                    request.session['user_loggedin'] = True
                    return redirect("dashboard")  # Redirect to dashboard
                else:
                    form.add_error(None, "Invalid password.")
    else:
        form = UserSignInForm()
    return render(request, 'SignIn.html', {'form': form})

def SignUp(request):
    
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            member = User(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Save the new User object to the database
            member.save()
            return redirect("/")
        else:
            # Print form errors to check if there are any validation errors
            print(form.errors)
    else:
        form = UserSignUpForm()
    
    return render(request, 'SignUp.html', {'form': form})


def Logout(request):

    if 'user_loggedin' in request.session:
        del request.session['user_loggedin']
        del request.session['user_id']
    return redirect("Main")