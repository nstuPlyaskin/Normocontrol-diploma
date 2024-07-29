from django import forms

from users.models import Group

from . import constants as cts
from .models import CheckOut, Remark


class RemarkNavForm(forms.Form):
    """Форма для указания страницы и абзаца замечания."""
    SECTION_CHOICES = (
        ('title', 'Титульный лист'),
        ('task', 'Индивидуальное задание на ВКР'),
        ('abstract', 'Реферат'),
        ('contents', 'Содержание'),
        ('introduction', 'Введение'),
        ('body', 'Основная часть'),
        ('conclusion', 'Заключение'),
        ('source', 'Список использованных источников'),
        ('attachment', 'Приложение'),
    )
    section = forms.ChoiceField(
        label='Раздел ПЗ',
        choices=SECTION_CHOICES)
    page_number = forms.CharField(
        label='Номер страницы',
        required=False)
    paragraph = forms.CharField(
        label='Номер абзаца',
        required=False)
    check_all = forms.BooleanField(
        label='Проверить по всей работе',
        required=False)
    custom_error = forms.CharField(
        label='Замечание:',
        widget=forms.Textarea(attrs={'style': 'height: 105px'}),
        required=False
    )


class RemarkEditForm(forms.ModelForm):
    """Форма редактирования замечания."""
    class Meta:
        model = Remark
        fields = ('section', 'page_number', 'paragraph', 'text',)


class RemarkStandartErrorForm(forms.Form):
    """Форма выбора замечания."""
    # [ERROR_MAIN]
    err_main_1 = forms.BooleanField(label=cts.ERROR_MAIN_1, required=False)
    err_main_2 = forms.BooleanField(label=cts.ERROR_MAIN_2, required=False)
    err_main_3 = forms.BooleanField(label=cts.ERROR_MAIN_3, required=False)
    err_main_4 = forms.BooleanField(label=cts.ERROR_MAIN_4, required=False)
    err_main_5 = forms.BooleanField(label=cts.ERROR_MAIN_5, required=False)
    err_main_6 = forms.BooleanField(label=cts.ERROR_MAIN_6, required=False)
    err_main_7 = forms.BooleanField(label=cts.ERROR_MAIN_7, required=False)
    err_main_8 = forms.BooleanField(label=cts.ERROR_MAIN_8, required=False)
    # [ERROR_TEXT]
    err_text_1 = forms.BooleanField(label=cts.ERROR_TEXT_1, required=False)
    err_text_2 = forms.BooleanField(label=cts.ERROR_TEXT_2, required=False)
    err_text_3 = forms.BooleanField(label=cts.ERROR_TEXT_3, required=False)
    err_text_4 = forms.BooleanField(label=cts.ERROR_TEXT_4, required=False)
    # [ERROR_HEADERS]
    err_header_1 = forms.BooleanField(label=cts.ERROR_HEAD_1, required=False)
    err_header_2 = forms.BooleanField(label=cts.ERROR_HEAD_2, required=False)
    err_header_3 = forms.BooleanField(label=cts.ERROR_HEAD_3, required=False)
    # [ERROR_LIST]
    err_list_1 = forms.BooleanField(label=cts.ERROR_LIST_1, required=False)
    # [ERROR_TABLE]
    err_table_1 = forms.BooleanField(label=cts.ERROR_TABLE_1, required=False)
    err_table_2 = forms.BooleanField(label=cts.ERROR_TABLE_2, required=False)
    err_table_3 = forms.BooleanField(label=cts.ERROR_TABLE_3, required=False)
    err_table_4 = forms.BooleanField(label=cts.ERROR_TABLE_4, required=False)
    # [ERROR_IMAGE]
    err_image_1 = forms.BooleanField(label=cts.ERROR_IMAGE_1, required=False)
    err_image_2 = forms.BooleanField(label=cts.ERROR_IMAGE_2, required=False)
    err_image_3 = forms.BooleanField(label=cts.ERROR_IMAGE_3, required=False)
    err_image_4 = forms.BooleanField(label=cts.ERROR_IMAGE_4, required=False)
    # [ERROR_FORMULA]
    err_formula_1 = forms.BooleanField(label=cts.ERROR_FORMULA_1,
                                       required=False)
    err_formula_2 = forms.BooleanField(label=cts.ERROR_FORMULA_2,
                                       required=False)
    err_formula_3 = forms.BooleanField(label=cts.ERROR_FORMULA_3,
                                       required=False)
    # [ERROR_FRAME]
    err_frame_1 = forms.BooleanField(label=cts.ERROR_FRAME_1, required=False)
    err_frame_2 = forms.BooleanField(label=cts.ERROR_FRAME_2, required=False)
    # [ERROR_LINK]
    err_link_1 = forms.BooleanField(label=cts.ERROR_LINK_1, required=False)
    err_link_2 = forms.BooleanField(label=cts.ERROR_LINK_2, required=False)


class CheckForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ('docx_file', 'pdf_file', 'info')

    def clean_docx_file(self):
        data = self.cleaned_data['docx_file']
        file_type = data.name.split('.')[-1]
        if file_type != 'docx':
            raise forms.ValidationError(
                'Файл должен иметь расширение .docx',
            )
        if data.size > 8000000:
            raise forms.ValidationError(
                'Файл должен иметь размер не более 8 Мб',
            )
        return data

    def clean_pdf_file(self):
        data = self.cleaned_data['pdf_file']
        file_type = data.name.split('.')[-1]
        if file_type != 'pdf':
            raise forms.ValidationError("Файл должен иметь расширение .pdf",
                                        code='invalid extension')
        if data.size > 8000000:
            raise forms.ValidationError(
                'Файл должен иметь размер не более 8 Мб',
            )
        return data


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title',)
