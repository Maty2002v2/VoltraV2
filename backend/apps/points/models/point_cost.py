from django.db import models


class PointCost(models.Model):
    START_ROW = 2
    EXPORT_START_ROW = 1
    IMPORT_MAPPER = {
        'read_month': 0,
        'previous_date': 1,
        'date': 2,
        'payer_number': 3,
        'tariff': 4,
        'usage': 5,
        'netto': 6,
        'vat': 7,
        'brutto': 8,
        'osd': 9,
        'payer_name': 10,
        'related_entity': 11,
        'payer_address_city': 12,
        'payer_address_street': 13,
        'trading_value': 14,
        'receiver_name': 15,
        'receiver_address_city': 16,
        'billing_cycle': 17,
        'receiver_address_street': 18,
        'nip': 19,
        'fv_number': 21,
    }

    read_month = models.IntegerField(verbose_name='Miesiąc odczytu')
    previous_date = models.DateField(verbose_name='Data poprzedniego odczytu')
    date = models.DateField(verbose_name='Data bieżącego odczytu')
    payer_number = models.CharField(verbose_name='Nr płatnika', max_length=100)
    tariff = models.CharField(verbose_name='Taryfa', max_length=100)
    usage = models.IntegerField(verbose_name='Ilość energii')
    netto = models.FloatField(verbose_name='Wartość netto')
    vat = models.FloatField(verbose_name='VAT')
    brutto = models.FloatField(verbose_name='Wartość brutto')
    osd = models.CharField(verbose_name='OSD', max_length=100)
    payer_name = models.CharField(verbose_name='Nazwa płatnika', max_length=100)
    related_entity = models.CharField(verbose_name='Powiązana jednostka', max_length=100)
    payer_address_city = models.CharField(verbose_name='Adres płatnika - miasto', max_length=100)
    payer_address_street = models.CharField(verbose_name='Adres płatnika - ulica', max_length=100)
    trading_value = models.FloatField(verbose_name='Wartość obrotu')
    receiver_name = models.CharField(verbose_name='Nazwa odbiorcy', max_length=100)
    receiver_address_city = models.CharField(verbose_name='Adres odbiorcy - miasto', max_length=100)
    billing_cycle = models.CharField(verbose_name='Cykl rozliczeniowy', max_length=100)
    receiver_address_street = models.CharField(verbose_name='Adres odbiorcy - ulica', max_length=100)
    nip = models.CharField(verbose_name='NIP', max_length=100)
    fv_number = models.CharField(verbose_name='Numer FV', max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    point = models.ForeignKey('points.Point', related_name='costs', on_delete=models.CASCADE, verbose_name='punkt')

    class Meta(object):
        verbose_name = 'koszt'
        verbose_name_plural = 'koszty'

    def __str__(self):
        return str(self.id)

    def to_excel(self):
        return [
            self.read_month,
            self.previous_date,
            self.date,
            self.payer_number,
            self.tariff,
            self.usage,
            self.netto,
            self.vat,
            self.brutto,
            self.osd,
            self.payer_name,
            self.related_entity,
            self.payer_address_city,
            self.payer_address_street,
            self.trading_value,
            self.receiver_name,
            self.receiver_address_city,
            self.billing_cycle,
            self.receiver_address_street,
            self.nip,
            self.point.ppe_number,
            self.fv_number,
        ]



class PointCostProxy(PointCost):
    class Meta:
        proxy = True
        verbose_name = "raport punktów"
        verbose_name_plural = "raporty punktów"
