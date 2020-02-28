from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView


class AdminView(AdminIndexView):

    @expose('/')
    def admin_index(self):
        return self.render('admin.html')


class UserView(ModelView):
    column_exclude_list = ('password',)
    column_labels = {
        'username': 'Username',
        'email': 'Почта',
        'password': 'Пароль',
    }
    create_modal = True
    edit_modal = True


class EventView(ModelView):
    column_labels = {
        'title': 'Название',
        'description': 'Описание',
        'date': 'Дата события',
        'time': 'Время события',
        'event_type': 'Тип события',
        'category': 'Категория',
        'address': 'Адрес проведения',
        'seats': 'Количество мест',
        'location': 'Место проведения',
        'participants': 'Участники',
        'enrollments': 'Регистрации',
    }
    column_editable_list = (
        'title',
        'seats',
        'description',
        'date',
        'time',
        'event_type',
        'category',
    )


class ParticipantView(ModelView):
    column_exclude_list = ('password',)
    column_labels = {
        'name': 'Имя участника',
        'email': 'Почта',
        'password': 'Пароль',
        'picture': 'Фото',
        'location': 'Город',
        'about': 'Информация о себе',
        'events': 'События',
        'enrollments': 'Регистрации',
    }


class EnrollmentView(ModelView):
    column_labels = {
        'registrated_at': 'Дата регистрации',
        'participant': 'Участник',
        'event': 'Событие',
    }


class LocationView(ModelView):
    column_labels = {
        'title': 'Город',
        'location_type': 'Код города',
        'events': 'События',
    }
    column_editable_list = ('title', 'location_type',)
