from django.urls import path
from . import views
from . import compilerView
urlpatterns = [
    path('',views.index),
    path('api/code/',compilerView.compiler)
]