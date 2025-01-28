from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User



class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:  # Если это email
            kwargs = {'email': username}
        else:  # Если это username
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)  # Получаем пользователя по email или username
            if user.check_password(password):  # Проверяем пароль
                return user
            return None
        except User.DoesNotExist:  # Если пользователь не найден
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)  # Находим пользователя по ID
        except User.DoesNotExist:
            return None