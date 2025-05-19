from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from apps.users.models.password_reset import PasswordResetToken
#from apps.users.models.user_profile import UserProfile
from apps.users.models.user import UserProfile
from apps.users.utils import reset_password_token
from apps.users.utils.send_mail import send_reset_password_mail

# Usuwamy domyślną rejestrację User i Group
admin.site.unregister(User)
admin.site.unregister(Group)


class UserAdminForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='Imię')
    last_name = forms.CharField(required=True, label='Nazwisko')
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Hasło')

    # Pole do edycji numeru klienta (pobierane z UserProfile)
    client_number = forms.CharField(required=False, label="Numer klienta")
    okaycrm_id = forms.CharField(required=False, label="OkayCRM ID")

    def clean_email(self):
        """ Walidacja e-maila - sprawdzamy, czy istnieje inny użytkownik z tym e-mailem """
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if email and self._is_username_with_email_exists(username=username, email=email):
            raise forms.ValidationError('Inny użytkownik ma już taki adres email')
        return email

    def save(self, commit=True):
        """ Zapis użytkownika oraz numeru klienta i OkayCRM ID w UserProfile """
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            # Aktualizujemy numer klienta i OkayCRM ID w UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.client_number = self.cleaned_data.get("client_number")
            profile.okaycrm_id = self.cleaned_data.get("okaycrm_id")
            profile.save()

        return user

    def _is_username_with_email_exists(self, username, email):
        return User.objects.filter(email__iexact=email).exclude(username__iexact=username).exists()

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """ Customowy panel admina dla modelu User """
    form = UserAdminForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_client_number', 'get_okaycrm_id', 'is_active', 'is_superuser')
    fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'is_superuser', 'client_number', 'okaycrm_id')

    def get_client_number(self, obj):
        """ Pobiera numer klienta z UserProfile """
        return obj.profile.client_number if hasattr(obj, "profile") else None
    get_client_number.short_description = "Numer klienta"

    def get_okaycrm_id(self, obj):
        """ Pobiera OkayCRM ID z UserProfile """
        return obj.profile.okaycrm_id if hasattr(obj, "profile") else None
    get_okaycrm_id.short_description = "OkayCRM ID"

    def save_model(self, request, obj, form, change):
        """ Tworzenie użytkownika i przypisanie mu tokena resetu hasła """
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        if is_new:
            password_reset = PasswordResetToken.objects.create(user=obj)
            token = reset_password_token.make_token(obj)
            password_reset.reset_token = token
            password_reset.save()

            send_reset_password_mail(obj, token)

            # Tworzymy profil użytkownika (jeśli nie istnieje)
            UserProfile.objects.get_or_create(user=obj)
