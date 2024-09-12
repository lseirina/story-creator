from django.shortcuts import (render, redirect,
                              get_object_or_404,)
from stories.models import Story, VoiceRecording
from stories.forms import (StoryForm,
                           VoiceRecordingForm,
                           EditTranscriptionForm,)
from django.http import HttpResponseForbidden
import os
import speech_recognition as sr


def transcribe_audio(audio_path):
    """Transcribe audio using offline CMU Sphinx."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return 'Could not understand audio.'
    except sr.RequestError as e:
        return f'Sphinx error: {e}'


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
    story = get_object_or_404(Story, id=story_id)
    if request.method == 'POST':
        form = VoiceRecordingForm(request.POST, request.FILES)
        if form.is_valid():
            recording = form.save(commit=False)
            recording.story = story
            recording.save()
            audio_file_path = recording.file.path
            transcription = transcribe_audio(audio_file_path)
            recording.transcription = transcription
            recording.save()
            return redirect('story_detail', story_id=story.id)
    else:
        form = VoiceRecordingForm()
    context = {
        'form': form,
        'story': story
    }
    return render(request, 'add_recording.html', context)


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


def delete_transcription(request, recording_id):
    """View for deleteing transcription."""
    recording = get_object_or_404(VoiceRecording, id=recording_id)
    if request.method == 'POST':
        recording.delete()
        return redirect(story_list)
    return render(request, 'delete_transcription.html', {'recording': recording})






















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
