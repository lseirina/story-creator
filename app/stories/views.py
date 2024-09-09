from django.shortcuts import render, redirect, get_object_or_404
from stories.models import Story, VoiceRecording
from stories.forms import (StoryForm,
                           VoiceRecordingForm,
                           EditTranscriptionForm,)


def story_list(request):
    """View for listings stories."""
    stories = Story.objects.all()
    return render(request, 'story_list.html', {'stories': stories})


def story_detail(request, story_id):
    """View for detail story."""
    story = Story.objects.get(id=story_id)
    return render(request, 'story_detail.html', {'story': story})


def create_story(request):
    """View to create a story."""
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('story_list')
        else:
            form = StoryForm()
    return render(request, 'create_story.html', {'form': form})


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
    return render(request, 'add_recording.html', {'form': form})


def edit_transcription(request, recording_id):
    """View to edit transcription."""
    recording = get_object_or_404(VoiceRecording, id=recording_id)
    if request.method == 'POST':
        form = EditTranscriptionForm(request.POST, instance=recording)
        if form.is_valid():
            form.save()
            return redirect('story_detail', story_id=recording.story.id)
    else:
        form = EditTranscriptionForm(instance=recording)
    context = {
        'form': form,
        'recording': recording,
    }
    return render(request, 'edit_transcription.html', context)


























# def edit_transcription(request, recording_id):
#     recording = get_object_or_404(VoiceRecording, id=recording_id)

#     if request.method == 'POST':
#         form = EditTranscriptionForm(request.POST, instance=recording)
#         if form.is_valid():
#             form.save()
#             return redirect('story_detail', story_id=recording.story.id)
#     else:
#         form = EditTranscriptionForm(instance=recording)

#     return render(request, 'stories/edit_transcription.html', {'form': form, 'recording': recording})

# добавить предсавление для put patch и story_detail помимо остальных
