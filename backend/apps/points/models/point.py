from django.db import models

from apps.points.consts import EMPTY_FIELD


class Point(models.Model):
    START_ROW = 5
    EXPORT_START_ROW = 4
    IMPORT_MAPPER = {
        'division_name': 1,
        'division_address': 2,
        'division_receiver': 3,
        'division_nip': 4,
        'division_company_address': 5,
        'name': 6,
        'city': 7,
        'street': 8,
        'street_number': 9,
        'zip_code': 10,
        'post': 11,
        'ppe_number': 12,
        'osd_number': 13,
        'counter_number': 14,
        'tariff': 15,
        'power': 16,
        'contract_duration': 17,
        'osd_next': 18,
        'seller_change': 19,
        'seller': 20,
        'contract_type': 21,
        'notice_period': 22,
        'termination_date': 23,
        'sale_start': 24,
        'sale_end': 25,
        'annual_consumption': 28
    }

    name = models.CharField(max_length=100, blank=True, verbose_name='nazwa')
    city = models.CharField(max_length=100, blank=True, verbose_name='miasto')
    street = models.CharField(max_length=100, blank=True, verbose_name='ulica')
    street_number = models.CharField(max_length=32, blank=True, verbose_name='nr')
    zip_code = models.CharField(max_length=32, blank=True, verbose_name='kod pocztowy')
    post = models.CharField(max_length=100, blank=True, verbose_name='poczta')
    ppe_number = models.CharField(max_length=100, blank=True, verbose_name='numer PPE')
    osd_number = models.CharField(max_length=100, blank=True, verbose_name='numer OSD')
    counter_number = models.CharField(max_length=100, blank=True, verbose_name='numer licznika')
    tariff = models.CharField(max_length=100, blank=True, verbose_name='taryfa')
    power = models.CharField(max_length=100, blank=True, verbose_name='moc umowna')
    osd_next = models.CharField(max_length=100, blank=True, verbose_name='nazwa lokalnego OSD')
    seller_change = models.CharField(max_length=100, blank=True, verbose_name='pierwsza / kolejna zmiana sprzedawcy')
    seller = models.CharField(max_length=100, blank=True, verbose_name='sprzedawca')
    contract_type = models.CharField(max_length=100, blank=True, verbose_name='typ umowy')
    notice_period = models.CharField(max_length=100, blank=True, verbose_name='okres wypowedzenia')
    contract_duration = models.CharField(max_length=100, blank=True, verbose_name='okres obowiązywania umowy')
    termination_date = models.DateField(null=True, blank=True, verbose_name='data zakończenia umowy')
    sale_start = models.DateField(null=True, blank=True, verbose_name='rozpoczęcie sprzedaży')
    sale_end = models.DateField(null=True, blank=True, verbose_name='zakończenie sprzedaży')
    verified = models.BooleanField(default=False, verbose_name='zweryfikowany')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    photovoltaics = models.BooleanField(default=False, help_text="Czy punkt posiada fotowoltaikę?")
    annual_consumption = models.DecimalField(max_digits=10, default=0.0, decimal_places=2, verbose_name="Zużycie roczne")
    #
    division = models.ForeignKey(
        'division.Division',
        related_name='points',
        on_delete=models.CASCADE,
        verbose_name='jednostka',
    )
    tags = models.ManyToManyField('points.Tag', related_name='points', blank=True, verbose_name='tagi')

    class Meta(object):
        verbose_name = 'punkt'
        verbose_name_plural = 'punkty'

    def address(self):
        address = filter(
            None,
            [self.city, self.street, self.street_number, self.zip_code, self.post],
        )
        return ', '.join(address) or '-'

    address.short_description = 'adres'

    def __str__(self):
        return '{id} - {name} - {division_name}'.format(id=self.pk, name=self.name, division_name=self.division.name)

    def to_excel(self):
        return [
            self.division.name,
            self.division.address,
            self.division.receiver,
            self.division.nip,
            self.division.company_address,
            self.name,
            self.city,
            self.street,
            self.street_number,
            self.zip_code,
            self.post,
            self.ppe_number,
            self.osd_number,
            self.counter_number,
            self.tariff,
            self.power,
            self.contract_duration,
            self.osd_next,
            self.seller_change,
            self.seller,
            self.contract_type,
            self.notice_period,
            self.termination_date,
            self.sale_start,
            self.sale_end,
            EMPTY_FIELD,
            EMPTY_FIELD,
            self.annual_consumption,

        ]

class PointProxy(Point):
    class Meta:
        proxy = True
        verbose_name = "zużycie"
        verbose_name_plural = "zużycie"


class PointProxyRaport(Point):
    class Meta:
        proxy = True
        verbose_name = "raport punktów"
        verbose_name_plural = "raporty punktów"

    def to_excel(self):
        return [
            self.division.name,
            self.division.address,
            self.division.receiver,
            self.division.nip,
            self.division.company_address,
            self.name,
            self.city,
            self.street,
            self.street_number,
            self.zip_code,
            self.post,
            self.ppe_number,
            self.osd_number,
            self.counter_number,
            self.tariff,
            self.power,
            self.contract_duration,
            self.osd_next,
            self.seller_change,
            self.seller,
            self.contract_type,
            self.notice_period,
            self.termination_date,
            self.sale_start,
            self.sale_end,
            EMPTY_FIELD,
            EMPTY_FIELD,
            self.annual_consumption,

        ]