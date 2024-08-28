from django.shortcuts import render, redirect
from stories.models import Story, VoiceRecording
from stories.forms import StoryForm, VoiceRecordingForm


def story_list(request):
    """View for listings stories."""
    stories = Story.objects.all()
    return render(request, 'stories/story_list.html', {'stories': stories})


def story_detail(request, story_id):
    """View for detail story."""
    story = Story.objects.get(id=story_id)
    return render(request, 'stories/story_detail.html', {'story': story})


def create_story(request):
    """View to create a story."""
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('story_list')
        else:
            form = StoryForm()
    return render(request, 'stories/create_story.html', {'form': form})


def add_recording(request, story_id):
    """View to add story recording."""
    if request.method == 'POST':
        form = VoiceRecordingForm(request.POST, request.FILES)
        if form.is_valid():
            recording = form.save(commit=False)
            recording.story_id = story_id
            recording.save()
            return redirect('story_detail', story_id=story_id)
        else:
            recording = VoiceRecordingForm()
    return render(request, 'stories/add_recording.html', {'form': form})


# добавить предсавление для put patch и story_detail помимо остальных


















































# from django.shortcuts import render, redirect
# from .forms import StoryForm, VoiceRecordingForm


# def create_story(request):
#     if request.method == 'POST':
#         form = StoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('story_list')
#     else:
#         form = StoryForm()
#     return render(request, 'stories/create_story.html', {'form': form})


# def add_recording(request, story_id):
#     if request.method == 'POST':
#         form = VoiceRecordingForm(request.POST, request.FILES)
#         if form.is_valid():
#             recording = form.save(commit=False)
#             recording.story_id = story_id
#             recording.save()
#             return redirect('story_detail', story_id=story_id)
#     else:
#         form = VoiceRecordingForm()
#     return render(request, 'stories/add_recording.html', {'form': form})