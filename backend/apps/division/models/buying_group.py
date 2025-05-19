from django.db import models
from django.utils.timezone import now

class BuyingGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='nazwa')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    divisions = models.ManyToManyField('division.Division', related_name='buying_groups', verbose_name='jednostki')

    class Meta(object):
        verbose_name = 'grupa zakupowa'
        verbose_name_plural = 'grupy zakupowe'

    def __str__(self):
        return self.name

class BuyingGroupLink(models.Model):
    buyinggroup = models.OneToOneField(  # Zamiana ForeignKey na OneToOneField
        'division.BuyingGroup',
        on_delete=models.CASCADE,
        related_name='link',
        verbose_name="Grupa zakupowa"
    )
    link = models.URLField(
        max_length=2048,
        verbose_name="Link do platformy zakupowej"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data utworzenia"
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data ostatniej modyfikacji"
    )

    class Meta:
        db_table = 'buyinggroup_links'
        verbose_name = "Link do platformy zakupowej"
        verbose_name_plural = "Linki do platform zakupowych"

    def __str__(self):
        return f"Link do grupy zakupowej: {self.buyinggroup.name}"