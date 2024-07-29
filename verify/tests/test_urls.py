from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from users.models import Group
from verify.models import CheckOut, Remark
from verify.tests import constants as cts

User = get_user_model()


class VerifyURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            'index': '/',
            'unknown_page': '/unknown_page/',
        }
        cls.urls_need_access = {
            'student_list': '/students/',
            'group_list': '/group/',
            'new_group': '/group/new_group/',
            'student_active_check': f'/students/{cls.controller}/',
            'group_students': f'/group/{cls.group.slug}/',
            'add_remark': (f'/user/{cls.controller}/{cls.checkout.id}/'
                           'add_remark/'),
            'delete_remark': (f'/user/{cls.controller}/{cls.checkout.id}/'
                              f'{cls.remark.id}/delete_remark/'),
            'check_archive': (f'/user/{cls.controller}/{cls.checkout.id}/'
                              'check_archive/'),
            'check_active': (f'/user/{cls.controller}/{cls.checkout.id}/'
                             'check_active/'),
        }
        cls.urls_user_check = {
            'new_check': f'/user/{cls.student_1}/new_check/',
            'check_delete': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                             'check_delete/'),
            'check_view': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                           'check_view/'),
            'archive': f'/user/{cls.student_1}/archive/',
            'check_list': f'/user/{cls.student_1}/check_list/',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client_1.force_login(VerifyURLTests.student_1)
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(VerifyURLTests.student_2)
        self.authorized_client_3 = Client()
        self.authorized_client_3.force_login(VerifyURLTests.controller)

    def test_unknown_url(self):
        """Проверяем доступность неизвестного url."""
        response = self.authorized_client_1.get(
            VerifyURLTests.static_url['unknown_page']
        )
        self.assertEqual(response.status_code, 404)

    def test_url_available_to_guest_user(self):
        """Страницы доступны любому пользователю."""
        url_for_guest_user = [
            VerifyURLTests.static_url['index'],
        ]
        for url in url_for_guest_user:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_not_available_to_guest_user(self):
        """Страницы не доступны гостевому пользователю."""
        url_for_guest_user = [
            VerifyURLTests.urls_need_access['student_list'],
            VerifyURLTests.urls_need_access['group_list'],
            VerifyURLTests.urls_need_access['new_group'],
            VerifyURLTests.urls_need_access['student_active_check'],
            VerifyURLTests.urls_need_access['group_students'],
            VerifyURLTests.urls_need_access['add_remark'],
            VerifyURLTests.urls_need_access['delete_remark'],
            VerifyURLTests.urls_need_access['check_archive'],
            VerifyURLTests.urls_need_access['check_active'],
            VerifyURLTests.urls_user_check['check_list'],
            VerifyURLTests.urls_user_check['archive'],
            VerifyURLTests.urls_user_check['new_check'],
            VerifyURLTests.urls_user_check['check_view'],
            VerifyURLTests.urls_user_check['check_delete'],
        ]
        for url in url_for_guest_user:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    302,
                    f'URL {url} работает некорректно.'
                )

    def test_url_redirect_guest_user_to_login(self):
        """Проверяем редирект на страницу логина для гостевого пользователя."""
        url_for_guest_user = [
            VerifyURLTests.urls_need_access['student_list'],
            VerifyURLTests.urls_need_access['group_list'],
            VerifyURLTests.urls_need_access['new_group'],
            VerifyURLTests.urls_need_access['student_active_check'],
            VerifyURLTests.urls_need_access['group_students'],
            VerifyURLTests.urls_need_access['add_remark'],
            VerifyURLTests.urls_need_access['delete_remark'],
            VerifyURLTests.urls_need_access['check_archive'],
            VerifyURLTests.urls_need_access['check_active'],
            VerifyURLTests.urls_user_check['check_list'],
            VerifyURLTests.urls_user_check['archive'],
            VerifyURLTests.urls_user_check['new_check'],
            VerifyURLTests.urls_user_check['check_view'],
            VerifyURLTests.urls_user_check['check_delete'],
        ]
        for url in url_for_guest_user:
            with self.subTest():
                response = self.guest_client.get(url, follow=True)
                expected = f"/auth/login/?next={url}"
                self.assertRedirects(response, expected)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_access_names = {
            VerifyURLTests.static_url['index']:
            'verify/index.html',
            VerifyURLTests.urls_need_access['student_list']:
            'verify/student_list.html',
            VerifyURLTests.urls_need_access['student_active_check']:
            'verify/student_active_check.html',
            VerifyURLTests.urls_need_access['group_list']:
            'verify/group_list.html',
            VerifyURLTests.urls_need_access['new_group']:
            'verify/new_group.html',
            VerifyURLTests.urls_need_access['group_students']:
            'verify/student_list.html',
        }
        templates_url_check_names = {
            VerifyURLTests.urls_user_check['check_list']:
            'verify/check_list.html',
            VerifyURLTests.urls_user_check['archive']:
            'verify/check_list.html',
            VerifyURLTests.urls_user_check['check_view']:
            'verify/check_view.html',
        }
        for reverse_name, template in templates_url_access_names.items():
            with self.subTest():
                response = self.authorized_client_3.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'{reverse_name} не использует шаблон {template}'
                )
        for reverse_name, template in templates_url_check_names.items():
            with self.subTest():
                response = self.authorized_client_1.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'{reverse_name} не использует шаблон {template}'
                )

    def test_url_not_available_to_student_user(self):
        """Страницы не доступны пользователю-студенту."""
        urls = [
            VerifyURLTests.urls_need_access['student_list'],
            VerifyURLTests.urls_need_access['group_list'],
            VerifyURLTests.urls_need_access['new_group'],
            VerifyURLTests.urls_need_access['student_active_check'],
            VerifyURLTests.urls_need_access['group_students'],
            VerifyURLTests.urls_need_access['add_remark'],
            VerifyURLTests.urls_need_access['delete_remark'],
            VerifyURLTests.urls_need_access['check_archive'],
            VerifyURLTests.urls_need_access['check_active'],
        ]
        for url in urls:
            with self.subTest():
                response = self.authorized_client_1.get(url)
                self.assertEqual(response.status_code, 403)

    def test_url_available_to_controller_user(self):
        """Страницы доступны нормоконтроллеру."""
        urls_200 = [
            VerifyURLTests.urls_need_access['student_list'],
            VerifyURLTests.urls_need_access['group_list'],
            VerifyURLTests.urls_need_access['new_group'],
            VerifyURLTests.urls_need_access['student_active_check'],
            VerifyURLTests.urls_need_access['group_students'],
        ]
        for url in urls_200:
            with self.subTest():
                response = self.authorized_client_3.get(url)
                self.assertEqual(response.status_code, 200)
        urls_302 = [
            VerifyURLTests.urls_need_access['add_remark'],
            VerifyURLTests.urls_need_access['delete_remark'],
            VerifyURLTests.urls_need_access['check_archive'],
            VerifyURLTests.urls_need_access['check_active'],
        ]
        for url in urls_302:
            with self.subTest():
                response = self.authorized_client_3.get(url)
                self.assertEqual(response.status_code, 302)

    def test_url_not_available_to_wrong_student_user(self):
        """Страницы одного студента не доступны другому студенту."""
        urls = [
            VerifyURLTests.urls_user_check['check_list'],
            VerifyURLTests.urls_user_check['archive'],
            VerifyURLTests.urls_user_check['new_check'],
            VerifyURLTests.urls_user_check['check_view'],
            VerifyURLTests.urls_user_check['check_delete'],
        ]
        for url in urls:
            with self.subTest():
                response = self.authorized_client_2.get(url)
                self.assertEqual(response.status_code, 403)

    def test_url_available_to_correct_student_user(self):
        """Страницы доступны пользователю-студенту."""
        urls_200 = [
            VerifyURLTests.urls_user_check['check_list'],
            VerifyURLTests.urls_user_check['archive'],
            VerifyURLTests.urls_user_check['check_view'],
        ]
        for url in urls_200:
            with self.subTest():
                response = self.authorized_client_1.get(url)
                self.assertEqual(response.status_code, 200, f'{url}')
        urls_302 = [
            VerifyURLTests.urls_user_check['new_check'],
            VerifyURLTests.urls_user_check['check_delete'],
        ]
        for url in urls_302:
            with self.subTest():
                response = self.authorized_client_1.get(url)
                self.assertEqual(response.status_code, 302, f'{url}')

    def test_url_new_check_redirect(self):
        """Проверка редиректа после создания новой заявки."""
        response = self.authorized_client_1.get(
            VerifyURLTests.urls_user_check['new_check'],
            follow=True
        )
        expected = VerifyURLTests.urls_user_check['check_list']
        self.assertRedirects(response, expected)

    def test_url_check_delete_redirect(self):
        """Проверка редиректа после удаления заявки на проверку."""
        response = self.authorized_client_1.get(
            VerifyURLTests.urls_user_check['check_delete'],
            follow=True
        )
        expected = VerifyURLTests.urls_user_check['check_list']
        self.assertRedirects(response, expected)

    def test_url_check_archive_redirect(self):
        """Проверка редиректа после архивации заявки на проверку."""
        response = self.authorized_client_3.get(
            VerifyURLTests.urls_need_access['check_archive'],
            follow=True
        )
        expected = f'/user/{self.controller}/check_list/'
        self.assertRedirects(response, expected)

    def test_url_add_remark_redirect(self):
        """Проверка редиректа после активации заявки на проверку."""
        response = self.authorized_client_3.get(
            VerifyURLTests.urls_need_access['add_remark'],
            follow=True
        )
        expected = f'/user/{self.controller}/{self.checkout.id}/check_view/'
        self.assertRedirects(response, expected)

    def test_url_delete_remark_redirect(self):
        """Проверка редиректа после активации заявки на проверку."""
        response = self.authorized_client_3.get(
            VerifyURLTests.urls_need_access['delete_remark'],
            follow=True
        )
        expected = f'/user/{self.controller}/{self.checkout.id}/check_view/'
        self.assertRedirects(response, expected)
