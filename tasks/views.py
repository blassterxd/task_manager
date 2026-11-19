from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, F, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def index(request):
    """Главная страница."""
    return render(request, 'tasks/index.html')


@login_required
def task_list(request):
    """Список задач текущего пользователя."""
    priority_rank = Case(
        When(priority=Task.Priority.HIGH, then=Value(0)),
        When(priority=Task.Priority.NORMAL, then=Value(1)),
        default=Value(2),
        output_field=IntegerField(),
    )
    tasks = (
        Task.objects.filter(owner=request.user)
        .annotate(priority_rank=priority_rank)
        .order_by(
            'completed',
            'priority_rank',
            F('due_date').asc(nulls_last=True),
            'id',
        )
    )
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    """Создание задачи: владелец назначается здесь, а не в форме."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, 'Задача создана.')
            return redirect('tasks:list')
    else:
        form = TaskForm()
    context = {'form': form, 'title': 'Новая задача'}
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_edit(request, task_id):
    """Редактирование своей задачи."""
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены.')
            return redirect('tasks:list')
    else:
        form = TaskForm(instance=task)
    context = {'form': form, 'title': 'Редактирование задачи'}
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_delete(request, task_id):
    """Удаление: GET показывает подтверждение, удаляет только POST."""
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача удалена.')
        return redirect('tasks:list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
@require_POST
def task_toggle(request, task_id):
    """Переключает состояние «выполнена» только методом POST."""
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.completed = not task.completed
    task.save(update_fields=['completed'])
    return redirect('tasks:list')