from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.MainPage_view),
    path('ApportNature/Parametres', views.ApportNatureParameters_view, name ='Parametres'),
    path('ApportNature/Parametres/Formulaires/<int:ANF_id>', views.ApportNatureFormulaires_view, name ='Formulaires')
]