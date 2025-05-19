from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Division(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100, verbose_name='nazwa')
    receiver = models.CharField(max_length=100, blank=True, verbose_name='odbiorca')
    nip = models.CharField(max_length=13, blank=True, verbose_name='NIP')
    address = models.CharField(max_length=255, blank=True, verbose_name='adres nabywcy')
    company_address = models.CharField(max_length=255, blank=True, verbose_name='adres do faktury')

    account = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='użytkownik',
        related_name='divisions',
    )

    class Meta(object):
        verbose_name = 'Jednostka'
        verbose_name_plural = 'Jednostki'

    def __str__(self):
        return self.name
