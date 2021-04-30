import os

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.views.generic import TemplateView
from django.shortcuts import render,redirect, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from .forms import PredictionForm, LoginForm, SignUpForm
from .models import Disease

import io
import base64
from base64 import decodestring
from PIL import Image

from model.predict import predict_disease


class UserRegistrationView(TemplateView):
    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        """Redirect to predict if logged in"""
        if request.user.is_authenticated:
            return redirect('/predict')
        return super(UserRegistrationView, self).get(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        cxt = super().get_context_data(**kwargs)
        cxt['form'] = SignUpForm()
        return cxt

    def post(self, request):
        msg = None
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "User Created"
        return render(request, self.template_name, {"form": form, "msg" : msg})

class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        """Redirect to predict if logged in"""
        if request.user.is_authenticated:
            return redirect('/predict')
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")


            user = None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass

            if user is not None and user.check_password(password):
                # Check if email is verified or not
                if user.is_active:
                    login(request, user)
                    return redirect("/predict")
                else:
                    msg = "Users banned."
            else:    
                msg = 'Invalid credentials'

        else:
            msg = 'Error validating the form'

        return render(request, self.template_name, {"form": form, "msg" : msg})




class PredictView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        cxt =  super().get_context_data(**kwargs)
        cxt['prediction_form'] = PredictionForm(None)
        return cxt
    
    def get_uploaded_image_and_predict(self, image):
        """
            @params: 
                image: image object from form
            @return:
                prediction, image_for_template_rendering
        """
        # get encoded image from buffer
        im = Image.open(image)
        data = io.BytesIO()
        im.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())

        # Save image for prediction
        with open(str(image), "wb") as fh:
            fh.write(decodestring(encoded_img_data))
        
        # Get image path and predict
        image_path = os.path.join(os.path.dirname(__file__), f'../{str(image)}')
        prediction = predict_disease(image_path)

        # remove file
        if os.path.exists(image_path):
            os.remove(image_path)
        
        return prediction, encoded_img_data.decode('utf-8')
    
    def post(self, request):
        cxt = {}
        prediction_form = PredictionForm(request.POST, request.FILES)

        if prediction_form.is_valid():
            image = prediction_form.cleaned_data['image']
            
            # Get predicted disease
            prediction, template_image = self.get_uploaded_image_and_predict(image)

            try:
                disease = Disease.objects.get(name=prediction)
                cxt['disease'] = disease
            except Exception as e:
                print(e)
            
            cxt['prediction_form'] = PredictionForm(None)
            cxt['prediction'] = prediction
            cxt['image'] = template_image
        else:
            cxt['prediction_form'] = prediction_form

        return render(request, "index.html", cxt)

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(PredictView, self).dispatch(*args, **kwargs)