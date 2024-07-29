from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from verify.decorators import user_access
from verify.models import CheckOut

User = get_user_model()


@login_required
@user_access
def student_list(request):
    """Выводит таблицу всех зарегистрированных студентов."""
    students = User.objects.all().exclude(username='admin')
    students = students.exclude(allow_manage=True)
    context = {'students': students}
    return render(request, 'verify/student_list.html', context)


@login_required
@user_access
def student_active_check(request, username):
    """Выводит активную заявку определенного студента."""
    student_check = CheckOut.objects.all().filter(status=False)
    student_check = student_check.filter(student__username=username).first()
    context = {'student_check': student_check}
    return render(request, 'verify/student_active_check.html', context)
