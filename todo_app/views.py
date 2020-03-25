from django.shortcuts import render, redirect, get_object_or_404
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(creator=request.user,
                                date_completed__isnull=True)
    return render(request, 'currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(creator=request.user,
                                date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, creator=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'GET':
        return render(request, 'viewtodo.html',
                      {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'viewtodo.html',
                          {'todo': todo,
                           'form': form,
                           'error': 'Bad data passed in. Try again.'})


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html',
                      {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.creator = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'createtodo.html',
                          {'form': TodoForm(),
                           'error': 'Bad data passed in. Try again.'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, creator=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, creator=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
