import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Page
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from normocontrol.settings.base import MEDIA_ROOT
from users.models import Group
from verify.models import CheckOut, Remark
from verify.tests import constants as cts

User = get_user_model()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=cts.GROUP_1_TITLE,
            slug=cts.GROUP_1_SLUG,
        )
        cls.student = User.objects.create(
            username=cts.USERNAME_1,
            group=cls.group,
            allow_manage=False,
        )
        cls.controller = User.objects.create(
            username=cts.USERNAME_3,
            allow_manage=True,
        )
        checks = [
            CheckOut(student=cls.student, info=str(i)) for i in range(13)
        ]
        CheckOut.objects.bulk_create(checks)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.student)
        cache.clear()

    def test_first_page_containse_ten_checks(self):
        """Проверка наличия 10 записей на 1 странице паджинатора"""
        response = self.authorized_client.get(
            reverse('verify:check_list', kwargs={'username': self.student})
        )
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        """Проверка наличия 3 записей на 2 странице паджинатора"""
        url = reverse('verify:check_list', kwargs={'username': self.student})
        response = self.authorized_client.get(f"{url}?page=2")
        self.assertEqual(len(response.context.get('page').object_list), 3)

    def test_second_page_show_correct_context(self):
        """Проверка содержания последней заявки на 2 странице паджинатора"""
        url = reverse('verify:check_list', kwargs={'username': self.student})
        expected_info = CheckOut.objects.last().info
        response = self.authorized_client.get(f"{url}?page=2")
        self.assertEqual(response.context.get('page')[2].info, expected_info)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class VerifyViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.group = Group.objects.create(
            title=cts.GROUP_1_TITLE,
            slug=cts.GROUP_1_SLUG,
        )
        cls.student_1 = User.objects.create(
            username=cts.USERNAME_1,
            group=cls.group,
            allow_manage=False,
        )
        cls.student_2 = User.objects.create(
            username=cts.USERNAME_2,
            group=cls.group,
            allow_manage=False,
        )
        cls.controller = User.objects.create(
            username=cts.USERNAME_3,
            allow_manage=True,
        )
        cls.checkout = CheckOut.objects.create(
            student=cls.student_1,
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
        cls.static_url = {
            'index': reverse('verify:index'),
        }
        cls.urls_need_access = {
            'student_list': reverse(
                'verify:student_list'
            ),
            'group_list': reverse(
                'verify:group_list'
            ),
            'new_group': reverse(
                'verify:new_group'
            ),
            'student_active_check': reverse(
                'verify:student_active_check',
                kwargs={
                    'username': cls.controller
                }
            ),
            'group_students': reverse(
                'verify:group_students',
                kwargs={
                    'slug': cls.group.slug
                }
            ),
            'add_remark': reverse(
                'verify:add_remark',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id
                }
            ),
            'delete_remark': reverse(
                'verify:delete_remark',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id,
                    'remark_id': cls.remark.id
                }
            ),
            'check_archive': reverse(
                'verify:check_archive',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id
                }
            ),
            'check_active': reverse(
                'verify:check_active',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id
                }
            ),
        }
        cls.urls_user_check = {
            'new_check': reverse(
                'verify:new_check',
                kwargs={
                    'username': cls.student_1
                }
            ),
            'check_delete': reverse(
                'verify:check_delete',
                kwargs={
                    'username': cls.student_1,
                    'check_id': cls.checkout.id
                }
            ),
            'check_view': reverse(
                'verify:check_view',
                kwargs={
                    'username': cls.student_1,
                    'check_id': cls.checkout.id
                }
            ),
            'archive': reverse(
                'verify:archive',
                kwargs={
                    'username': cls.student_1
                }
            ),
            'check_list': reverse(
                'verify:check_list',
                kwargs={
                    'username': cls.student_1
                }
            ),
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.student_client_1 = Client()
        self.student_client_1.force_login(VerifyViewsTests.student_1)
        self.student_client_2 = Client()
        self.student_client_2.force_login(VerifyViewsTests.student_2)
        self.controller_client = Client()
        self.controller_client.force_login(VerifyViewsTests.controller)
        cache.clear()

    def test_new_check_show_in_correct_student_page(self):
        """Новая заявка отображается у корректного студента и нормоконтроллера.
        """
        CheckOut.objects.all().delete()
        CheckOut.objects.create(
            student=VerifyViewsTests.student_1,
            info=cts.INFO,
            status=False,
            docx_file=None,
            pdf_file=None,
        )
        checks_count = CheckOut.objects.all().count()
        response = self.student_client_1.get(
            VerifyViewsTests.urls_user_check['check_list']
        )

        self.assertEqual(
            len(response.context.get('page').object_list), checks_count
        )
        response = self.controller_client.get(
            reverse(
                'verify:check_list',
                kwargs={
                    'username': VerifyViewsTests.controller
                }
            ),
        )
        self.assertEqual(
            len(response.context.get('page').object_list), checks_count
        )
        response = self.student_client_2.get(
            VerifyViewsTests.urls_user_check['check_list']
        )
        self.assertIsNone(response.context.get('page'))

    def test_page_student_list_show_correct_context(self):
        """Страница student_list возвращает верный контекст."""
        response = self.controller_client.get(
            VerifyViewsTests.urls_need_access['student_list']
        )
        students_count = User.objects.all().exclude(allow_manage=True).count()
        self.assertEqual(
            response.context.get('students').count(), students_count
        )
        student_1_username = VerifyViewsTests.student_1.username
        self.assertEqual(
            response.context.get('students')[0].username, student_1_username
        )

    def test_page_group_list_show_correct_context(self):
        """Страница group_list возвращает верный контекст."""
        response = self.controller_client.get(
            VerifyViewsTests.urls_need_access['group_list']
        )
        group_count = Group.objects.count()
        self.assertEqual(
            response.context.get('group_list').count(), group_count
        )
        group_slug = VerifyViewsTests.group.slug
        self.assertEqual(
            response.context.get('group_list')[0].slug, group_slug
        )

    def test_page_group_students_show_correct_context(self):
        """Страница group_students возвращает верный контекст."""
        response = self.controller_client.get(
            VerifyViewsTests.urls_need_access['group_students']
        )
        group_slug = VerifyViewsTests.group.slug
        self.assertEqual(
            response.context.get('group').slug, group_slug
        )
        all_users = User.objects.all()
        group_students_count = all_users.filter(group=self.group).count()
        self.assertEqual(
            response.context.get('students').count(), group_students_count
        )

    def test_page_check_list_show_correct_context(self):
        """Страница check_list возвращает верный контекст."""
        response = self.student_client_1.get(
            VerifyViewsTests.urls_user_check['check_list']
        )
        CheckOut.objects.create(
            student=VerifyViewsTests.student_1,
            info=cts.INFO,
            status=True,
            docx_file=None,
            pdf_file=None,
        )
        checks_count = CheckOut.objects.all().filter(status=False).count()
        self.assertEqual(
            len(response.context.get('page').object_list), checks_count
        )
        self.assertTrue(response.context.get('active'))
        student_username = VerifyViewsTests.student_1.username
        self.assertEqual(response.context.get('username'), student_username)
        self.assertIsInstance(response.context.get('page'), Page)

    def test_page_student_active_check_show_correct_context(self):
        """Страница student_active_check возвращает верный контекст."""
        response = self.controller_client.get(
            reverse(
                'verify:student_active_check',
                kwargs={'username': self.student_1}
            )
        )
        check = CheckOut.objects.all().filter(
            status=False,
            student=VerifyViewsTests.student_1
        ).first()
        self.assertEqual(response.context.get('student_check'), check)

    def test_page_archive_show_correct_context(self):
        """Страница archive возвращает верный контекст."""
        CheckOut.objects.create(
            student=VerifyViewsTests.student_1,
            info=cts.INFO,
            status=True,
            docx_file=None,
            pdf_file=None,
        )
        response = self.student_client_1.get(
            VerifyViewsTests.urls_user_check['archive']
        )
        checks_count = CheckOut.objects.all().filter(
            status=True,
            student=VerifyViewsTests.student_1
        ).count()
        self.assertEqual(
            len(response.context.get('page').object_list), checks_count
        )
        self.assertFalse(response.context.get('active'))
        student_username = VerifyViewsTests.student_1.username
        self.assertEqual(response.context.get('username'), student_username)
        self.assertIsInstance(response.context.get('page'), Page)

    def test_page_check_view_show_correct_context(self):
        """Страница check_view возвращает верный контекст."""
        response = self.student_client_1.get(
            VerifyViewsTests.urls_user_check['check_view']
        )
        self.assertEqual(
            response.context.get('check_item').info,
            VerifyViewsTests.checkout.info
        )
        remarks_count = Remark.objects.all().filter(
            check_out=VerifyViewsTests.checkout
        ).count()
        self.assertEqual(
            response.context.get('remarks').count(), remarks_count
        )
        self.assertEqual(
            response.context.get('remarks').first().text,
            VerifyViewsTests.remark.text
        )
        student_username = VerifyViewsTests.student_1.username
        self.assertEqual(response.context.get('username'), student_username)

    def test_check_archive_change_status_to_true(self):
        """Заявка отправляется в архив."""
        new_check = CheckOut.objects.create(
            student=VerifyViewsTests.student_1,
            info=cts.INFO,
            status=False,
            docx_file=None,
            pdf_file=None,
        )
        self.controller_client.get(
            reverse(
                'verify:check_archive',
                kwargs={
                    'username': VerifyViewsTests.controller,
                    'check_id': new_check.id
                }
            ),
            follow=True
        )
        new_check.refresh_from_db()
        self.assertTrue(new_check.status)

    def test_check_active_change_status_to_false(self):
        """Заявка становится активной."""
        new_check = CheckOut.objects.create(
            student=VerifyViewsTests.student_1,
            info=cts.INFO,
            status=True,
            docx_file=None,
            pdf_file=None,
        )
        self.controller_client.get(
            reverse(
                'verify:check_active',
                kwargs={
                    'username': VerifyViewsTests.controller,
                    'check_id': new_check.id
                }
            ),
            follow=True
        )
        new_check.refresh_from_db()
        self.assertFalse(new_check.status)

    def test_check_delete_working(self):
        """Заявка удаляется."""
        new_check = CheckOut.objects.create(
            student=VerifyViewsTests.student_1,
            info=cts.INFO,
            status=False,
            docx_file=None,
            pdf_file=None,
        )
        checks_count = CheckOut.objects.count()
        self.controller_client.get(
            reverse(
                'verify:check_delete',
                kwargs={
                    'username': VerifyViewsTests.controller,
                    'check_id': new_check.id
                }
            ),
            follow=True
        )
        self.assertEqual(checks_count - 1, CheckOut.objects.count())

    def test_remark_delete_working(self):
        """Замечание удаляется."""
        new_remark = Remark.objects.create(
            section=cts.REMARK_SECTION,
            page_number=cts.REMARK_PAGE_NUMBER,
            paragraph=cts.REMARK_PARAGRAPH,
            text=cts.REMARK_TEXT,
            author=VerifyViewsTests.controller,
            check_out=VerifyViewsTests.checkout
        )
        remarks_count = Remark.objects.count()
        self.controller_client.get(
            reverse(
                'verify:delete_remark',
                kwargs={
                    'username': VerifyViewsTests.controller,
                    'check_id': VerifyViewsTests.checkout.id,
                    'remark_id': new_remark.id
                }
            ),
            follow=True
        )
        self.assertEqual(remarks_count - 1, Remark.objects.count())
