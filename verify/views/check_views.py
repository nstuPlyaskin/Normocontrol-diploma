from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail

from verify.decorators import user_access, user_check
from verify.forms import CheckForm, RemarkNavForm, RemarkStandartErrorForm
from verify.models import CheckOut
from django.contrib.auth.models import User

User = get_user_model()


@login_required
@user_check
def check_list(request, username):
    """Выводит список активных заявок для запрошенного пользователя."""
    user = get_object_or_404(User, username=username)
    check_list = CheckOut.objects.all().filter(status=False)
    if not user.allow_manage:
        check_list = check_list.filter(student__username=username)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'active': True, 'username': username}
    return render(request, 'verify/check_list.html', context)


@login_required
@user_check
def archive(request, username):
    """Выводит список архивных заявок для запрошенного пользователя."""
    user = get_object_or_404(User, username=username)
    check_list = CheckOut.objects.all().filter(status=True)
    if not user.allow_manage:
        check_list = check_list.filter(student__username=username)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'active': False, 'username': username}
    return render(request, 'verify/check_list.html', context)


@login_required
@user_check
def check_view(request, username, check_id):
    """Выводит данные по конкретной заявке для запрошенного пользователя."""
    # Формы под вопросом
    check_item = get_object_or_404(CheckOut, id=check_id)
    form_1 = RemarkNavForm(request.POST or None)
    form_2 = RemarkStandartErrorForm(request.POST or None)
    remarks = check_item.remark.all()
    context = {
        'username': username,
        'check_item': check_item,
        'remarks': remarks,
        'form_1': form_1,
        'form_2': form_2,
    }
    return render(request, 'verify/check_view.html', context)


@login_required
@user_access
def check_archive(request, username, check_id):
    """Отправляет определенную заявку в архив."""
    check_item = get_object_or_404(CheckOut, id=check_id)
    check_item.status = True
    check_item.pdf_file.delete()
    check_item.docx_file.delete()
    check_item.save()
    return redirect('verify:check_list', username)


@login_required
@user_access
def check_active(request, username, check_id):
    """Делает определенную заявку активной."""
    check_item = get_object_or_404(CheckOut, id=check_id)
    check_item.status = False
    check_item.save()
    return redirect('verify:check_list', username)


@login_required
@user_check
def check_delete(request, username, check_id):
    """Удаляет определенную заявку из БД."""
    get_object_or_404(CheckOut, id=check_id).delete()
    return redirect('verify:check_list', username)


@login_required
@user_check
def new_check(request, username):
    """Создает новую заявку от лица текущего пользователя."""
    student_check = request.user.checkout_student
    if student_check.exists() and not student_check.last().status:
        return redirect('verify:check_list', username)
    form = CheckForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'verify/new_check.html', {'form': form})
    check = form.save(commit=False)
    check.student = request.user
    check.save()

    # sending msg to superuser mail

    superusers = User.objects.filter(is_superuser=True)

    if superusers.exists():
        subject = 'Hовый запрос на проверку работы!'
        message = f'Hовый запрос на проверку работы от {request.user.username}!'
        from_email = 'pinkdumpyou@gmail.com'  # !!! REPLACE THIS EMAIL TO UR !!! ###########!!!!!!!!!!!!!!!!!

    for superuser in superusers:
        to_email = superuser.email
        send_mail(subject, message, from_email, [to_email])

        # DEBUG OUT HOW MANY MSGS WAS SESNDED TO SUPERUSERS EMAIL
        # print("superuser email: ", to_email)

    return redirect('verify:check_list', username)

