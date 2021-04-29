from django.urls import path, include

from .views import PredictView
urlpatterns = [
    path('predict', PredictView.as_view())
    
]
