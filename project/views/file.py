from datetime import date

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from project.forms import TaskForm, FileForm
from project.models import Task, Project, Team, Activity, FileManager, Objective


def index(request):
    form = FileForm()
    file = FileManager.objects.all().filter(project__user=request.user)
    project = Project.objects.all().filter(user=request.user)
    context = {
        'form': form,
        'files': 'active',
        'file': file,
        'project': project
    }
    return render(request, 'file/index.html', context)


@csrf_exempt
def fileCreate(request):
    form = FileForm()
    context = {}
    file = FileManager.objects.all().filter(project__user=request.user)
    project = Project.objects.all().filter(user=request.user)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            context = {
                'form': form,
                'files': 'active',
                'file': file,
                'project': project
            }
            return render(request, 'file/fileList.html', context)
    context.__setitem__('fuck', 'u too')
    return render(request, 'file/fileList.html', context)


def fileDelete(request, id):
    t = FileManager.objects.get(id=id)
    t.delete()
    messages.success(request, 'Your file was deleted successfully!')
    return redirect(reverse('project:file'))


def fileFilter(request, id):
    form = FileForm()
    if str(id) == '0':
        return redirect(reverse('project:file'))
    all_project = Project.objects.all().filter(user=request.user)
    all_files = FileManager.objects.all().filter(project=str(id))
    context = {
        'form': form,
        'files': 'active',
        'file': all_files,
        'project': all_project,
    }
    return render(request, 'file/index.html', context)


@csrf_exempt
def fileUpdate(request, id):
    data = {}
    data['form_is_valid'] = False
    project = Project.objects.all().filter(user=request.user)
    file = FileManager.objects.get(id=id)
    form = FileForm(instance=file)
    if request.POST:
        form = FileForm(request.POST, instance=file)
        if form.is_valid():
            form.save()
            file = FileManager.objects.all().filter(project__user=request.user)
            context = {
                'files': 'active',
                'file': file,
                'project': project
            }
            data['form_is_valid'] = True
            data['sms'] = 'Your File was successfully updated!'
            data['project_task'] = render_to_string('file/fileList.html', context)
            return JsonResponse(data)
    context = {
        'project': project,
        'form': form,
        'file': file
    }
    data['html_form'] = render_to_string('file/file_create.html', context)
    return JsonResponse(data)


def fileDetail(request, id):
    file = FileManager.objects.get(id=id)
    context={
        'file':file,
        'files':'active'
    }
    return render(request, 'file/file_detail.html', context)
