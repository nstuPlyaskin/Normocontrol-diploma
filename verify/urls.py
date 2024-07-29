from django.urls import path

from . import views


app_name = 'verify'

# Главные страницы
urlpatterns = [
     path('', views.index, name='index')
]

# Студенты
urlpatterns += [
     path('students/',
          views.student_list,
          name='student_list'),
     path('students/<str:username>/',
          views.student_active_check,
          name='student_active_check'),
]

# Группы
urlpatterns += [
     path('group/',
          views.group_list,
          name='group_list'),
     path('group/new_group/',
          views.new_group,
          name='new_group'),
     path('group/<slug:slug>/',
          views.group_students,
          name='group_students'),
]

# Проверки
urlpatterns += [
     path('user/<str:username>/check_list/',
          views.check_list,
          name='check_list'),
     path('user/<str:username>/archive/',
          views.archive,
          name='archive'),
     path('user/<str:username>/new_check/',
          views.new_check,
          name='new_check'),
     path('user/<str:username>/<int:check_id>/check_view/',
          views.check_view,
          name='check_view'),
     path('user/<str:username>/<int:check_id>/check_delete/',
          views.check_delete,
          name='check_delete'),
     path('user/<str:username>/<int:check_id>/check_archive/',
          views.check_archive,
          name='check_archive'),
     path('user/<str:username>/<int:check_id>/check_active/',
          views.check_active,
          name='check_active'),
]


# Замечания
urlpatterns += [
     path('user/<str:username>/<int:check_id>/add_remark/',
          views.add_remark,
          name='add_remark'),
     path('user/<str:username>/<int:check_id>/<int:remark_id>/delete_remark/',
          views.delete_remark,
          name='delete_remark'),
     path('user/<str:username>/<int:check_id>/<int:remark_id>/edit_remark/',
          views.edit_remark,
          name='edit_remark'),
]
