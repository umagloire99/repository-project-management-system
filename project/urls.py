from django.conf.urls import re_path

from project.views import team, file, expense
from . import viewed
from .views import task

app_name = 'project'

urlpatterns = [
    re_path(r'^project/$', viewed.project, name='project'),
    re_path(r'^project/category/(?P<filter>.+)$', viewed.projectFilter, name='category'),
    re_path(r'^project/create$', viewed.project_create, name='create'),
    re_path(r'^project/(?P<id>\d+)/delete$', viewed.project_delete, name='delete'),
    re_path(r'^project/(?P<id>\d+)/update$', viewed.project_update, name='update'),
    re_path(r'^project/detail/(?P<id>\d+)$', viewed.project_detail, name='detail'),
    re_path(r'^tasks/$', task.taskList, name='task'),
    re_path(r'^tasks/assigned$', task.taskListAssigned, name='task_assigned'),
    re_path(r'^tasks/(?P<id>\d+)/$', task.taskProject, name='task_project'),
    re_path(r'^tasks/(?P<id>\d+)/(?P<filter>.+)$', task.taskStatus, name='task_state'),
    re_path(r'^project/tasks/create$', task.task_create, name='task_create'),
    re_path(r'^project/tasks/(?P<id>\d+)/(?P<state>.+)/state$', task.object_state, name='objective_state'),
    re_path(r'^project/tasks/(?P<id>\d+)/delete$', task.task_delete, name='task_delete'),
    re_path(r'^project/tasks/(?P<id>\d+)/update$', task.task_update, name='task_update'),
    re_path(r'^project/tasks/(?P<id>\d+)/objective/create$', task.object_create, name='objective_create'),
    re_path(r'^project/tasks/(?P<id>\d+)/objective/delete$', task.object_delete, name='objective_delete'),
    re_path(r'^project/tasks/(?P<id>\d+)/objective/complete$', task.obj_complete, name='objective_complete'),
    re_path(r'^project/tasks/(?P<id>\d+)/objective/update$', task.object_update, name='objective_update'),
    re_path(r'^task/detail/(?P<id>\d+)$', task.taskDetail, name='task_detail'),
    re_path(r'^team/$', team.index, name='team'),
    re_path(r'^team/(?P<id>\d+)$', team.teamFilter, name='team_filter'),
    re_path(r'^team/(?P<id>\d+)/delete$', team.teamDelete, name='team_delete'),
    re_path(r'^project/team/(?P<id>\d+)/create$', team.teamCreate, name='team_create'),
    re_path(r'^project/team/update/(?P<id>\d+)/$', team.teamUpdate, name='team_update'),
    re_path(r'^files/$', file.index, name='file'),
    re_path(r'^files/(?P<id>\d+)$', file.fileDetail, name='file_detail'),
    re_path(r'^project/files/create$', file.fileCreate, name='file_create'),
    re_path(r'^files/(?P<id>\d+)/delete$', file.fileDelete, name='file_delete'),
    re_path(r'^files/index/(?P<id>\d+)$', file.fileFilter, name='file_filter'),
    re_path(r'^files/(?P<id>\d+)/update$', file.fileUpdate, name='file_update'),
    re_path(r'^resources/$', expense.index, name='expense'),
    re_path(r'^project/resource/create$', expense.expense_create, name='expense_create'),
    re_path(r'^resources/(?P<id>\d+)$', expense.expenseUpdate, name='expense_update'),
    re_path(r'^expenses/index/(?P<id>\d+)$', expense.expenseFilter, name='expense_filter'),
    re_path(r'^expenses/(?P<id>\d+)/delete$', expense.expenseDelete, name='expense_delete'),

]