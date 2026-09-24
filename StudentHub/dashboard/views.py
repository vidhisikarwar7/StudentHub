from django.shortcuts import render, redirect
from .models import Task, Note, StudyMaterial, StudyPlan

def home(request):

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        material_title = request.POST.get('material_title', '').strip()
        study_file = request.FILES.get('study_file')
        subject = request.POST.get('subject', '').strip()
        topic = request.POST.get('topic', '').strip()
        study_date = request.POST.get('study_date')
        study_time = request.POST.get('study_time')

        if title:
            Task.objects.create(title=title)

        if content:
            Note.objects.create(content=content)

        if material_title and study_file:
            StudyMaterial.objects.create(
                title=material_title,
                file=study_file
            )
        if subject and topic and study_date and study_time:
          StudyPlan.objects.create(
           subject=subject,
           topic=topic,
           study_date=study_date,
           study_time=study_time
    )

        return redirect('home')

    tasks = Task.objects.all()
    notes = Note.objects.all()
    materials = StudyMaterial.objects.all()
    study_plans = StudyPlan.objects.all().order_by('study_date', 'study_time')

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()

    return render(request, 'dashboard/home.html', {
    'tasks': tasks,
    'notes': notes,
    'materials': materials,
    'study_plans': study_plans,
    'total_tasks': total_tasks,
    'completed_tasks': completed_tasks
})


def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()

    return redirect('home')


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()

    return redirect('home')


def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()

    return redirect('home')
def delete_material(request, material_id):
    material = StudyMaterial.objects.get(id=material_id)

    if material.file:
        material.file.delete(save=False)

    material.delete()

    return redirect('home')
def complete_plan(request, plan_id):
    plan = StudyPlan.objects.get(id=plan_id)
    plan.completed = True
    plan.save()

    return redirect('home')


def delete_plan(request, plan_id):
    plan = StudyPlan.objects.get(id=plan_id)
    plan.delete()

    return redirect('home')