from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Task


def task_list(request):
    task = Task.objects.all().order_by("-created_at")
    return render(request, "todo/task_list.html", {"tasks": task})


def task_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        discription = request.POST.get("description", "").strip()
        # description=request.POST.get('description','')
        if title:
            Task.objects.create(title=title, description=discription)
            return redirect(reverse("todo:task_list"))
        error = "Title cannot be empty."
        return render(request, "todo/task_form.html", {"error": error})
    return render(request, "todo/task_form.html")


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        discription = request.POST.get("description", "").strip()
        completed = request.POST.get("completed") == "on"
        if title:
            task.title = title
            task.description = discription
            task.completed = completed
            task.save()
            return redirect(reverse("todo:task_list"))
        return render(
            request,
            "todo/task_form.html",
            {"task": task, "error": "title cannot be empty."},
        )
    return render(request, "todo/task_form.html", {"task": task})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect(reverse("todo:task_list"))
    return render(request, "todo/task_confirm_delete.html", {"task": task})


def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
        return redirect("todo:task_list")
