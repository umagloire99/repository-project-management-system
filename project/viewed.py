from datetime import date
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from project.forms import ProjectForm
from project.models import Project, Team, Task, Role, Inventory, Activity, FileManager

DOCUMENT_FILE_TYPES = ['doc', 'docx', 'pdf']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def save_all(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            project = form.save(commit=False)
            d = project.endDate - project.startDate
            project.user = request.user
            project.remaining = project.budget
            project.days = int(d.days)
            project.save()
            new_Team, created = Team.objects.get_or_create(
                user=request.user,
                member=request.user,
                project=project
            )
            new_Team.role.add(Role.objects.get(id=1))
            new_Activity, created = Activity.objects.get_or_create(
                user=request.user,
                action='created a new project',
                all_activity=project.name
            )
            new_Activity.target.add(request.user)
            data['form_is_valid'] = True
            data['sms'] = "The project was successfully added!"
            p = Project.objects.all().filter(user=request.user)
            data['project_list'] = render_to_string('project/ProjectList.html', {'p': p}, request=request)
        else:
            data['form_is_valid'] = False
    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@csrf_exempt
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
    else:
        form = ProjectForm()
    return save_all(request, form, 'project/project_create.html')


def project(request):
    Project.objects.filter(progressbar=100).update(category='Completed')
    Project.objects.filter(Q(progressbar__lt=100) & Q(category='Completed')).update(category='In Progress')

    progress = "border-color: #358E35; color: #358E35"
    complete = "border-color: #28aac2; color: #28aac2"
    cancel = "border-color: #da2222; color: #da2222"
    pro = Project.objects.all().filter(user=request.user)

    context = {
        'complete': complete,
        'cancel': cancel,
        'progress': progress,
        'p': pro,
        'project': 'active'
    }
    return render(request, 'project/project.html', context)


def projectFilter(request, filter):
    progress = "border-color: #358E35; color: #358E35"
    complete = "border-color: #28aac2; color: #28aac2"
    cancel = "border-color: #da2222; color: #da2222"
    all = "border-color: black; color: black"
    pro = Project.objects.all().filter(user=request.user)
    p = pro.filter(category=filter)
    if filter == 'In Progress':
        context = {
            'complete': complete,
            'cancel': cancel,
            'all': all,
            'p': p,
            'project': 'active'
        }
    elif filter == 'Completed':
        context = {
            'progress': progress,
            'cancel': cancel,
            'all': all,
            'p': p,
            'project': 'active'
        }
    elif filter == 'Cancelled':
        context = {
            'complete': complete,
            'progress': progress,
            'all': all,
            'p': p,
            'project': 'active'
        }
    return render(request, 'project/project.html', context)


@csrf_exempt
def project_delete(request, id):
    data = {}
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        team = Team.objects.all().filter(Q(user=request.user) & Q(project=project))
        new_Activity, created = Activity.objects.get_or_create(
            user=request.user,
            action='deleted the project',
            all_activity=project.name
        )
        for t in team:
            new_Activity.target.add(t.member)
        project.delete()
        data['form_is_valid'] = True
        data['sms'] = "The project was successfully deleted!"
        p = Project.objects.all().filter(user=request.user)
        data['project_list'] = render_to_string('project/ProjectList.html', {'p': p}, request=request)
    else:
        data['html_form'] = render_to_string('project/project_delete.html', {'project': project}, request=request)
    return JsonResponse(data)


def project_update(request, id):
    data = {}
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            data['sms'] = "The project was successfully updated!"
            project = form.save(commit=False)
            d = project.endDate - project.startDate
            if int(d.days) <= 0:
                project.days = 0
            else:
                project.days = int(d.days)
            team = Team.objects.all().filter(Q(user=request.user) & Q(project=project))
            new_Activity, created = Activity.objects.get_or_create(
                user=request.user,
                action='updated a project',
                all_activity=project.name
            )
            for t in team:
                new_Activity.target.add(t.member)
            project.save()
            data['form_is_valid'] = True
            p = Project.objects.all().filter(user=request.user)
            data['project_list'] = render_to_string('project/ProjectList.html', {'p': p}, request=request)
        else:
            data['form_is_valid'] = False
    form = ProjectForm(instance=project)
    data['html_form'] = render_to_string('project/project_update.html', {'project': project, 'form': form},
                                         request=request)
    return JsonResponse(data)


def project_detail(request, id):
    project = Project.objects.get(id=id)
    inventory = Inventory.objects.all().filter(Q(user=request.user) & Q(project=project))
    expense = 0
    for i in inventory:
        expense = expense + i.cost
    user = User.objects.all().filter(Q(team__user=request.user) & Q(team__project=project))
    team = Team.objects.all().filter(Q(user=request.user) & Q(project=project))
    total_task = Task.objects.all().filter(Q(user=request.user) & Q(project=project)).count()
    upcoming = Task.objects.all().filter(Q(user=request.user) & Q(project=project) & Q(due_date__gte=date.today()))
    overdue = Task.objects.all().filter(Q(user=request.user) & Q(project=project) & Q(due_date__lt=date.today()))
    activity = Activity.objects.all().filter(user=request.user)
    file = FileManager.objects.all().filter(Q(user=request.user) & Q(project=project))
    remain = project.budget - expense
    print(remain)
    if remain <= 0:
        remain = 0
    Project.objects.filter(id=id).update(remaining=remain)
    context = {
        'file': file,
        'activity': activity,
        'upcoming': upcoming,
        'overdue': overdue,
        'remain': remain,
        'expense': expense,
        'user': user,
        'project': 'active',
        'team': team,
        'total_task': total_task,
        'p': project
    }
    return render(request, 'project/projectDetail.html', context)
