from datetime import date
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from project.forms import TaskForm
from project.models import Task, Project, Team, Activity, FileManager, Objective


def taskList(request):
    task = Task.objects.all().filter(user=request.user)
    project_task = Project.objects.all().filter(user=request.user)
    context = {
        'tasks': 'active',
        'task': task,
        'id': 0,
        'project': project_task
    }
    return render(request, 'tasks/index.html', context)


def taskListAssigned(request):
    task = Task.objects.all().filter(member__username=request.user)
    print(task)
    project_task = Project.objects.all().filter(task__member__username=request.user)
    context = {
        'tasks_a': 'active',
        'task': task,
        'id': 0,
        'project': project_task
    }
    return render(request, 'tasks/index.html', context)


def taskProject(request, id):
    project = Project.objects.all().filter(user=request.user)
    if id == 0:
        return redirect(reverse('project:task'))
    else:
        project_task = Task.objects.all().filter(Q(project=id) & Q(user=request.user))
        context = {
            'tasks': 'active',
            'task': project_task,
            'project': project,
            'id': id,
        }
        return render(request, 'tasks/index.html', context)


def taskStatus(request, id, filter):
    project = Project.objects.all().filter(user=request.user)
    if id == '0':
        if filter == 'all':
            return redirect(reverse('project:task'))
        else:
            project_task = Task.objects.all().filter(Q(user=request.user) &
                                                     Q(status=filter))
    else:
        if filter == 'all':
            return redirect(reverse('project:task'))
        else:
            project_task = Task.objects.all().filter(Q(project=id) & Q(user=request.user) &
                                                     Q(status=filter))
    context = {
        'tasks': 'active',
        'task': project_task,
        'project': project,
        'id': id
    }
    return render(request, 'tasks/index.html', context)


@csrf_exempt
def task_create(request):
    name_error = ""
    date_error = ""
    context = {}
    data = {}
    data['form_is_valid'] = False
    myproject = Project.objects.all().filter(user=request.user)
    user = User.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            project = form.cleaned_data['project']
            due_date = form.cleaned_data['due_date']
            start_date = form.cleaned_data['start_date']
            pro = Project.objects.get(id=str(project))
            if Task.objects.all().filter(Q(user=request.user) & Q()
                                         & Q(name=name) & Q(project=project)):
                name_error = "This Task exist already in that project"
            elif Task.objects.all().filter(
                    Q(Q(project__endDate__lt=due_date) | Q(project__endDate__lt=start_date)) & Q(user=request.user)):
                date_error = "Check your start date and your due date! " \
                             + "the project start on the " + str(
                    pro.startDate) + " and end on the " + str(pro.endDate)
            else:

                ta = form.save(commit=False)
                ta.user = request.user
                ta.save()
                form.save_m2m()
                task = Task.objects.all().filter(user=request.user)
                project_task = Project.objects.all().filter(user=request.user)
                context = {
                    'tasks': 'active',
                    'task': task,
                    'id': 0,
                    'project': project_task
                }
                data['form_is_valid'] = True
                data['sms'] = 'Your Task was successfully added!'
                data['project_task'] = render_to_string('tasks/taskList.html', context, request=request)
                return JsonResponse(data)
    else:
        form = TaskForm()
    context = {
        'myproject': myproject,
        'myname': name_error,
        'mydate': date_error,
        'user': user,
        'form': form
    }
    data['html_form'] = render_to_string('tasks/task_create.html', context, request=request)
    return JsonResponse(data)


def task_update(request, id):
    date_error = ""
    myproject = Project.objects.all().filter(user=request.user)
    data = {}
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            project = form.cleaned_data['project']
            due_date = form.cleaned_data['due_date']
            start_date = form.cleaned_data['start_date']
            pro = Project.objects.get(id=str(project))
            if Task.objects.all().filter(
                    Q(Q(project__endDate__lt=due_date) | Q(project__endDate__lt=start_date)) & Q(user=request.user)):
                date_error = "Check your start date and your due date! " \
                             + "the project start on the " + str(
                    pro.startDate) + " and end on the " + str(pro.endDate)
            else:

                ta = form.save(commit=False)
                ta.save()
                form.save_m2m()
                task = Task.objects.all().filter(user=request.user)
                project_task = Project.objects.all().filter(user=request.user)
                context = {
                    'tasks': 'active',
                    'task': task,
                    'id': 0,
                    'project': project_task
                }
                data['form_is_valid'] = True
                data['sms'] = 'Your Task was successfully updated!'
                data['project_task'] = render_to_string('tasks/taskList.html', context, request=request)
                return JsonResponse(data)
    else:
        form = TaskForm(instance=task)
    context = {
        'myproject': myproject,
        'task': task,
        'mydate': date_error,
        'user': User.objects.all(),
        'form': form
    }
    data['html_form'] = render_to_string('tasks/task_edit.html', context, request=request)
    return JsonResponse(data)


@csrf_exempt
def task_delete(request, id):
    t = Task.objects.get(id=id)
    team = Team.objects.all().filter(Q(user=request.user) & Q(project=t.project))
    new_Activity, created = Activity.objects.get_or_create(
            user=request.user,
            action='deleted the task',
            all_activity=t.name
        )
    for team in team:
        new_Activity.target.add(team.member)
    t.delete()
    return redirect(reverse('project:task'))


def taskDetail(request, id):
    objects = Objective.objects.all().filter(task=id)
    complet = Objective.objects.all().filter(Q(task=id) & Q(complete=True))
    if objects:
        progress = int((complet.count() / objects.count()) * 100)
        Task.objects.filter(id=id).update(progressbar=progress)
    Task.objects.filter(progressbar=100).update(status='Completed')
    t = Task.objects.get(id=id)
    all_task = Task.objects.all().filter(project=t.project).count()
    completed_task = Task.objects.all().filter(Q(project=t.project) & Q(status='Completed')).count()
    if all_task != 0:
        task_percent = int((completed_task / all_task) * 100)
        Project.objects.filter(id=str(t.project)).update(progressbar=task_percent)
    file = FileManager.objects.all().filter(task=t)
    obj = Objective.objects.all().filter(task=t)
    if request.method == 'POST' and request.POST.get('outline') is not None:
        new_Objective, created = Objective.objects.get_or_create(
            title=request.POST.get('title'),
            outline=request.POST.get('outline'),
            task=t
        )
        for user in t.member.all():
            if request.POST.get(str(user)) is not None:
                new_Objective.user.add(user)
        sms = "The objective was successfully added "
        obj = Objective.objects.all().filter(task=t)
        context = {'tasks': 'active',
                   't': t, 'obj': obj,
                   'file': file, 'sms': sms}
        return render(request, 'tasks/taskDetail.html', context)
    t = Task.objects.get(id=id)
    context = {'tasks': 'active',
               't': t, 'obj': obj,
               'file': file}
    print(context)
    return render(request, 'tasks/taskDetail.html', context)


def object_create(request, id):
    t = Task.objects.get(id=id)
    file = FileManager.objects.all().filter(task=t)
    data = {}
    t = Task.objects.get(id=id)
    if request.method == 'POST':
        new_Objective, created = Objective.objects.get_or_create(
            title=request.POST.get('title'),
            outline=request.POST.get('outline'),
            task=t
        )
        for user in t.member.all():
            if request.POST.get(str(user)) is not None:
                new_Objective.user.add(user)
        sms = "The objective was successfully added "
        obj = Objective.objects.all().filter(task=t)
        data['obje'] = True
        data['sms'] = sms
        data['objective'] = render_to_string('tasks/objectiveList.html', {'obj': obj}, request=request)
        return JsonResponse(data)
    else:
        data['html_form'] = render_to_string('tasks/objective_create.html', {'t': t}, request=request)
    return JsonResponse(data)


def object_update(request, id):
    data = {}
    obj = Objective.objects.get(id=id)
    t = Task.objects.get(id=str(obj.task))
    if request.method == 'POST':
        new_Objective, created = Objective.objects.get_or_create(
            id=request.POST.get('obj_id')
        )
        new_Objective.user.clear()
        for user in t.member.all():
            if request.POST.get(str(user)) is not None:
                new_Objective.user.add(user)
        new_Objective.save()
        Objective.objects.filter(id=request.POST.get('obj_id')).update(
            title=request.POST.get('title'),
            outline=request.POST.get('outline')
        )
        sms = "The objective was successfully updated "
        obj = Objective.objects.all().filter(task=t)
        data['obje'] = True
        data['sms'] = sms
        data['objective'] = render_to_string('tasks/objectiveList.html', {'obj': obj}, request=request)
        return JsonResponse(data)
    else:
        data['html_form'] = render_to_string('tasks/objective_update.html', {'obj': obj, 't': t}, request=request)
    return JsonResponse(data)


def object_delete(request, id):
    obj = Objective.objects.get(id=id)
    task = obj.task
    obj.delete()
    return redirect(reverse('project:task_detail', kwargs={'id': task}))


def obj_complete(request, id):
    obj = Objective.objects.get(id=id)
    task = obj.task
    Objective.objects.filter(id=id).update(complete=True)

    return redirect(reverse('project:task_detail', kwargs={'id': task}))


def object_state(request, id, state):
    Task.objects.filter(id=id).update(status=state)
    task = Task.objects.get(id=id)
    return redirect(reverse('project:task_detail', kwargs={'id': task}))
