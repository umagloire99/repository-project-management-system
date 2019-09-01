from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Q
from django.db.models.signals import pre_save
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here

class Project(models.Model):
    types = [('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    name = models.CharField(max_length=50)
    icon = models.ImageField(null=True, blank=True)
    description = RichTextUploadingField()
    progressbar = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=100, choices=types, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.PositiveIntegerField(default=0)
    remaining = models.PositiveIntegerField(default=0, editable=False)
    startDate = models.DateField(auto_now=False)
    endDate = models.DateField(auto_now=False)
    days = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-added_at']


class Calendar(models.Model):
    event_name = models.CharField(max_length=100, verbose_name='Event name')
    event_desc = RichTextField(config_name='default', verbose_name='Event description')
    start_date = models.DateField(auto_now=False, verbose_name='Start Date')
    end_date = models.DateField(auto_now=False, verbose_name='End Date')
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.event_name)

    class Meta:
        ordering = ['-added_at']


class Task(models.Model):
    user = models.CharField(max_length=50)
    types = [('New', 'New'), ('On Hold', 'On Hold'), ('In Progress', 'In Progress'), ('Completed', 'Completed'),
             ('Cancelled', 'Cancelled')]
    pin = models.BooleanField(default=False)
    name = models.CharField(max_length=50, verbose_name='Title:')
    description = RichTextUploadingField(config_name='other', verbose_name='Description:')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project:')
    status = models.CharField(max_length=200, choices=types, verbose_name='Status:')
    member = models.ManyToManyField(User, verbose_name='Member:')
    start_date = models.DateField(auto_now=False, verbose_name='Start Date:')
    due_date = models.DateField(auto_now=False, verbose_name='Due date:')
    progressbar = models.PositiveSmallIntegerField(verbose_name='Progressbar:', default=0, null=True, blank=True)
    days = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-added_at']


class FileManager(models.Model):
    file_name = models.CharField(max_length=500)
    upload_file = models.FileField()
    note = RichTextField(config_name='short')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    types = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-added_at']


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.name


class Team(models.Model):
    user = models.CharField(max_length=50)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-added_at']


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = RichTextField(config_name='default')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ['-added_at']


class Inventory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    total_cost = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    note = RichTextField(config_name='default')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-added_at']


class Activity(models.Model):
    user = models.CharField(max_length=500)
    action = models.CharField(max_length=100)
    all_activity = models.CharField(max_length=500)
    added_at = models.DateTimeField(auto_now_add=True)
    target = models.ManyToManyField(User)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ['-added_at']


class Objective(models.Model):
    title = models.CharField(max_length=100)
    outline = models.TextField()
    user = models.ManyToManyField(User)
    added_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-added_at']


def pre_save_FileManager(sender, instance, *args, **kwargs):
    AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
    IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
    DOCUMENT_FILE_TYPES = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls']
    path = instance.upload_file.url.split('.')[-1]
    if str(path).lower() in IMAGE_FILE_TYPES:
        instance.types = 'image/' + str(path)
    elif str(path).lower() in DOCUMENT_FILE_TYPES:
        instance.types = 'document/' + str(path)
    elif str(path).lower() in AUDIO_FILE_TYPES:
        instance.types = 'audio/' + str(path)
    else:
        instance.types = 'video/' + str(path)


def pre_save_tasks(sender, instance, *args, **kwargs):
    d = instance.due_date - instance.start_date
    instance.days = int(d.days)
    all_task = Task.objects.all().filter(project=instance.project).count()
    completed_task = Task.objects.all().filter(Q(project=instance.project) & Q(status='Completed')).count()

    if all_task != 0:
        task_percent = int((completed_task / (all_task + 1)) * 100)
        Project.objects.filter(id=str(instance.project)).update(progressbar=task_percent)


def pre_save_objective(sender, instance, *args, **kwargs):
    obj = Objective.objects.all().filter(task=str(instance.task))
    complet = Objective.objects.all().filter(Q(task=str(instance.task)) & Q(complete=True))
    if obj:
        progress = int((complet.count() / (obj.count() + 1)) * 100)
        if progress == 100:
            Task.objects.filter(id=str(instance.task)).update(progressbar=progress, status='Completed')
        else:
            Task.objects.filter(id=str(instance.task)).update(progressbar=progress, status='In Progress')


pre_save.connect(pre_save_objective, sender=Objective)
pre_save.connect(pre_save_tasks, sender=Task)
pre_save.connect(pre_save_FileManager, sender=FileManager)
