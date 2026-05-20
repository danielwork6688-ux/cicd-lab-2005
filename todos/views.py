from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo


def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todos/index.html', {'todos': todos})


def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Todo.objects.create(title=title)
    return redirect('todo_list')


def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')
