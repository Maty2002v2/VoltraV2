from django.contrib.auth import get_user_model

User = get_user_model()


def make_user(username='username', email='email@email.com', password='1234', **kwargs):
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        **kwargs,
    )
