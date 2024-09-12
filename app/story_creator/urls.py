"""story_creator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stories import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', views.create_story, name='create_story'),
    path('stories/', views.story_list, name='story_list'),
    path('stories/<int:story_id>', views.story_detail, name='story_detail'),
    path('<int:story_id>/add_recording/', views.add_recording, name='add_recording'),
    path('<int:recording_id>/edit/',
         views.edit_transcription, name='edit_transcription'),
    path('<int:recording_id>/delete/', views.delete_transcription,
         name='delete')

]
