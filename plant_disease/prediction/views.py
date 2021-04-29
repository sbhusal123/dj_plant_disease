import os
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import PredictionForm

from model.predict import predict_disease

import io
import base64
from base64 import decodestring
from PIL import Image



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
            
            prediction, template_image = self.get_uploaded_image_and_predict(image)

            
            cxt['prediction_form'] = PredictionForm(None)
            cxt['prediction'] = prediction
            cxt['image'] = template_image
        else:
            cxt['prediction_form'] = prediction_form

        return render(request, "index.html", cxt)

