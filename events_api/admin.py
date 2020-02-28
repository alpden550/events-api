from flask import flash, redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from events_api.form import LoginForm


class AdminView(AdminIndexView):

    @expose('/')
    def admin_index(self):
        return self.render('admin.html')

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm()
        if request.method == 'POST':
            from events_api.models import User
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.validate_password(form.password.data):
                flash('Неверное имя пользователя или пароль')
                return self.render('auth.html', form=form)
            return redirect(url_for('admin.admin_index'))

        return self.render('auth.html', form=form)


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
    column_editable_list = ('title', 'location_type')
