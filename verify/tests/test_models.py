from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import CustomUser, Group
from verify.models import CheckOut, Remark
from verify.tests import constants as cts

User = get_user_model()


class VerifyModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=cts.GROUP_1_TITLE,
            slug=cts.GROUP_1_SLUG,
        )
        cls.student = CustomUser.objects.create(
            username=cts.USERNAME_1,
            group=cls.group,
            allow_manage=False,
        )
        cls.controller = CustomUser.objects.create(
            username=cts.USERNAME_2,
            allow_manage=True,
        )
        cls.checkout = CheckOut.objects.create(
            student=cls.student,
            info=cts.INFO,
            status=False,
            docx_file=None,
            pdf_file=None,
        )
        cls.remark = Remark.objects.create(
            section=cts.REMARK_SECTION,
            page_number=cts.REMARK_PAGE_NUMBER,
            paragraph=cts.REMARK_PARAGRAPH,
            text=cts.REMARK_TEXT,
            author=cls.controller,
            check_out=cls.checkout
        )

    def test_checkout_object_name(self):
        """Имя объекта через __str__ является строкой вида check__id."""
        expected_object_name = f'check_{VerifyModelTest.checkout.id}'
        self.assertEquals(expected_object_name, str(VerifyModelTest.checkout))

    def test_checkout_verbose_name(self):
        """verbose_name в полях модели Checkout совпадает с ожидаемым."""
        field_verboses = {
            'student': CheckOut._meta.get_field('student').verbose_name,
            'check_date': CheckOut._meta.get_field('check_date').verbose_name,
            'info': CheckOut._meta.get_field('info').verbose_name,
            'status': CheckOut._meta.get_field('status').verbose_name,
            'docx_file': CheckOut._meta.get_field('docx_file').verbose_name,
            'pdf_file': CheckOut._meta.get_field('pdf_file').verbose_name,
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                field = VerifyModelTest.checkout._meta.get_field(value)
                self.assertEqual(field.verbose_name, expected)

    def test_checkout_help_text(self):
        """help_text в полях модели Checkout совпадает с ожидаемым."""
        field_help_texts = {
            'student': CheckOut._meta.get_field('student').help_text,
            'check_date': CheckOut._meta.get_field('check_date').help_text,
            'info': CheckOut._meta.get_field('info').help_text,
            'status': CheckOut._meta.get_field('status').help_text,
            'docx_file': CheckOut._meta.get_field('docx_file').help_text,
            'pdf_file': CheckOut._meta.get_field('pdf_file').help_text,
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                field = VerifyModelTest.checkout._meta.get_field(value)
                self.assertEqual(field.help_text, expected)

    def test_remark_object_name(self):
        """Имя объекта через __str__ является строкой вида remark__id."""
        expected_object_name = f'remark_{VerifyModelTest.remark.id}'
        self.assertEquals(expected_object_name, str(VerifyModelTest.remark))

    def test_remark_verbose_name(self):
        """verbose_name в полях модели Remark совпадает с ожидаемым."""
        field_verboses = {
            'section': Remark._meta.get_field('section').verbose_name,
            'page_number': Remark._meta.get_field('page_number').verbose_name,
            'paragraph': Remark._meta.get_field('paragraph').verbose_name,
            'check_all': Remark._meta.get_field('check_all').verbose_name,
            'text': Remark._meta.get_field('text').verbose_name,
            'author': Remark._meta.get_field('author').verbose_name,
            'check_out': Remark._meta.get_field('check_out').verbose_name,
            'check_date': Remark._meta.get_field('check_date').verbose_name,
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                field = VerifyModelTest.remark._meta.get_field(value)
                self.assertEqual(field.verbose_name, expected)

    def test_remark_help_text(self):
        """help_text в полях модели Remark совпадает с ожидаемым."""
        field_help_texts = {
            'section': Remark._meta.get_field('section').help_text,
            'page_number': Remark._meta.get_field('page_number').help_text,
            'paragraph': Remark._meta.get_field('paragraph').help_text,
            'check_all': Remark._meta.get_field('check_all').help_text,
            'text': Remark._meta.get_field('text').help_text,
            'author': Remark._meta.get_field('author').help_text,
            'check_out': Remark._meta.get_field('check_out').help_text,
            'check_date': Remark._meta.get_field('check_date').help_text,
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                field = VerifyModelTest.remark._meta.get_field(value)
                self.assertEqual(field.help_text, expected)
