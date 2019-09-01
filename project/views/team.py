from datetime import date
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from project.forms import TeamForm
from project.models import Team, Project, Role
from django.contrib import messages


def index(request):
    team = Team.objects.all().filter(user=request.user)
    project = Project.objects.all().filter(user=request.user)
    roles = Role.objects.all()
    users = User.objects.get(username=request.user)
    context = {
        'teams': 'active',
        'users': users,
        'team': team,
        'all_project': project,
        'project': project,
        'roles': roles
    }
    return render(request, 'team/index.html', context)


def teamFilter(request, id):
    if str(id) == '0':
        return redirect(reverse('project:team'))
    team = Team.objects.all().filter(Q(user=request.user) & Q(project=id))
    project = Project.objects.all().filter(Q(user=request.user) & Q(id=id))
    all_project = Project.objects.all().filter(user=request.user)
    roles = Role.objects.all()
    users = User.objects.get(username=request.user)
    context = {
        'teams': 'active',
        'users': users,
        'team': team,
        'project': project,
        'all_project': all_project,
        'roles': roles
    }
    return render(request, 'team/index.html', context)


def teamDelete(request, id):
    t = Team.objects.get(id=id)
    t.delete()
    messages.success(request, 'Your member was deleted successfully!')
    return redirect(reverse('project:team'))


@csrf_exempt
def teamUpdate(request, id):
    if request.method == 'POST':
        for team in Team.objects.all().filter(project=id):
            if request.POST.get(str(team.id)):
                new_Team, created = Team.objects.get_or_create(
                    id=team.id
                )
                new_Team.role.clear()
                for role in Role.objects.all():
                    print(new_Team)
                    if request.POST.get(str(role)+str(team.id)):
                        new_Team.role.add(role)
            new_Team.save()
    messages.success(request, 'Your members was updated successfully!')
    return redirect(reverse('project:team'))


@csrf_exempt
def teamCreate(request, id):
    data = {}
    form = TeamForm()
    users = User.objects.all()
    project = Project.objects.all().filter(user=request.user)
    member = Team.objects.all().filter(user=request.user)
    for member in member:
        users = users.exclude(username=member.member)
    users = User.objects.all().exclude(username=request.user)
    context = {
        'member': member,
        'users': users,
        'project': project,
        'form': form
    }
    data['html_form'] = render_to_string('team/team_create.html', context, request)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.user = request.user
            team.save()
            form.save_m2m()
            messages.success(request, 'Your member was added successfully!')
            if str(id) == '0':
                return redirect(reverse('project:team'))
            else:
                return redirect(reverse('project:detail', kwargs={'id': id}))
        else:
            messages.warning(request, 'Add a permissions for each member!')
            return redirect(reverse('project:team'))
    return JsonResponse(data)
