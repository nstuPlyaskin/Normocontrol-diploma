from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from verify.decorators import user_access
from verify.forms import RemarkEditForm, RemarkNavForm, RemarkStandartErrorForm
from verify.models import CheckOut, Remark


@login_required
@user_access
def add_remark(request, username, check_id):
    """Добавляет замечание на основе формы."""
    check_item = get_object_or_404(CheckOut, id=check_id)
    form_1 = RemarkNavForm(request.POST or None)
    form_2 = RemarkStandartErrorForm(request.POST or None)
    if form_1.is_valid() and form_2.is_valid():
        choice = form_1.cleaned_data['section']
        section = dict(form_1.fields['section'].choices)[choice]
        page_number = form_1.cleaned_data.get('page_number')
        paragraph = form_1.cleaned_data.get('paragraph')
        check_all = form_1.cleaned_data.get('check_all')
        custom_error = form_1.cleaned_data.get('custom_error')
        # Создаем кастомную ошибку, если это требуется
        if custom_error != '':
            check_all_status = None
            if check_all:
                check_all_status = form_1.fields.get('check_all').label,
            Remark.objects.get_or_create(
                section=section,
                page_number=page_number,
                paragraph=paragraph,
                check_all=check_all_status,
                text=custom_error,
                author=request.user,
                check_out=check_item
            )
        # Проверяем поля формы и создаем ошибки
        for field in form_2.fields:
            checkbox_result = form_2.cleaned_data.get(field)
            if checkbox_result:
                check_all_status = None
                if check_all:
                    check_all_status = form_1.fields.get('check_all').label,
                Remark.objects.get_or_create(
                    section=section,
                    page_number=page_number,
                    paragraph=paragraph,
                    check_all=check_all_status,
                    text=form_2.fields.get(field).label,
                    author=request.user,
                    check_out=check_item
                )
    return redirect('verify:check_view', username, check_id)


@login_required
@user_access
def edit_remark(request, username, check_id, remark_id):
    """Редактирует замечание."""
    remark = get_object_or_404(Remark, id=remark_id)
    form = RemarkEditForm(request.POST or None, instance=remark)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'verify/edit_remark.html', context)
    remark.save()
    return redirect('verify:check_view', username, check_id)


@login_required
@user_access
def delete_remark(request, username, check_id, remark_id):
    """Удаляет замечание."""
    remark = get_object_or_404(Remark, id=remark_id)
    remark.delete()
    return redirect('verify:check_view', username, check_id)
