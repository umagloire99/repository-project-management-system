from datetime import date

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from project.forms import TaskForm, FileForm, InventoryForm
from project.models import Task, Project, Team, Activity, FileManager, Objective, Inventory


def index(request):
    all_inventory = Inventory.objects.all().filter(user=request.user)
    myproject = Project.objects.all().filter(user=request.user)
    context = {
        'project': myproject,
        'all_inventory': all_inventory,
        'expenses': 'active',
    }
    return render(request, 'expenses/index.html', context)


@csrf_exempt
def expense_create(request):
    data = {}
    data['form_is_valid'] = False
    form = InventoryForm()
    myproject = Project.objects.all().filter(user=request.user)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.total_cost = expense.cost * expense.quantity
            p = Project.objects.get(id=str(expense.project))
            if p.budget != 0:
                if expense.total_cost > p.remaining:
                    error_sms = 'Your remaining budget is:' + str(p.remaining) + ' and your total cost is: ' + str(expense.total_cost)
                    context = {
                        'error_sms':error_sms,
                        'myproject': myproject,
                        'form': form
                    }
                    data['html_form'] = render_to_string('expenses/expense_create.html', context, request=request)
                    return JsonResponse(data)
                p.remaining = p.remaining - expense.total_cost
            expense.save()
            all_inventory = Inventory.objects.all().filter(user=request.user)
            context = {
                'all_inventory': all_inventory
            }
            data['form_is_valid'] = True
            data['sms'] = 'Your item was successfully added!'
            data['project_list'] = render_to_string('expenses/expenseList.html', context, request=request)
            return JsonResponse(data)
    context = {
        'myproject': myproject,
        'form': form
    }
    data['html_form'] = render_to_string('expenses/expense_create.html', context, request=request)
    return JsonResponse(data)


@csrf_exempt
def expenseUpdate(request, id):
    inventory = Inventory.objects.get(id=id)
    myproject = Project.objects.all().filter(user=request.user)
    form = InventoryForm(instance=inventory)
    if request.POST:
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.total_cost = expense.cost * expense.quantity
            p = Project.objects.get(id=str(expense.project))
            if p.budget != 0:
                if expense.total_cost > p.remaining:
                    messages.warning(request, 'Your remaining budget is:' + str(p.remaining) + ' and your total cost is: ' + str(
                        expense.total_cost))
                    context = {
                        'myproject': myproject,
                        'form': form
                    }
                    return redirect(reverse('project:expense_update', kwargs={'id': id}))
            expense.user = request.user
            expense.total_cost = expense.cost * expense.quantity
            expense.save()
            messages.success(request, 'Your resource was update successfully!')
            return redirect(reverse('project:expense_update', kwargs={'id': id}))

    context = {
        'inventory':inventory,
        'expenses': 'active',
        'myproject': myproject,
        'form': form
    }
    return render(request, 'expenses/expenseDetail.html', context)


def expenseFilter(request, id):
    if str(id) == '0':
        return redirect(reverse('project:expense'))

    all_inventory = Inventory.objects.all().filter(user=request.user, project=id)
    myproject = Project.objects.all().filter(user=request.user)
    context = {
        'project': myproject,
        'all_inventory': all_inventory,
        'expenses': 'active',
    }
    return render(request, 'expenses/index.html', context)


def expenseDelete(request, id):
    e = Inventory.objects.get(id=id)
    e.delete()
    messages.success(request, 'Your resource was deleted successfully!')
    return redirect(reverse('project:expense'))
