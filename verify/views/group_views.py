from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from users.models import Group
from verify.decorators import user_access
from verify.forms import GroupForm


@login_required
@user_access
def group_list(request):
    """Выводит таблицу всех зарегистрированных групп."""
    group_list = Group.objects.all()
    context = {'group_list': group_list}
    return render(request, 'verify/group_list.html', context)


@login_required
@user_access
def group_students(request, slug):
    """Выводит таблицу студентов заданной группы."""
    group = get_object_or_404(Group, slug=slug)
    students = group.user.all()
    context = {'students': students, 'group': group}
    return render(request, 'verify/student_list.html', context)


@login_required
@user_access
def new_group(request):
    """Создает новую студенческую группу."""
    form = GroupForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'verify/new_group.html', {'form': form})
    form.save()
    return redirect('verify:check_list', request.user.username)
