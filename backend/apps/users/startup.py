from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def setup_sync_users_cron():
    # Tworzymy interwał co 10 minut
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.MINUTES,
    )

    # Rejestrujemy (lub aktualizujemy) zadanie
    PeriodicTask.objects.update_or_create(
        name='Synchronizacja użytkowników z CRM',
        defaults={
            'interval': schedule,
            'task': 'apps.users.tasks.sync_users_from_okaycrm',
            'args': json.dumps([]),
            'kwargs': json.dumps({}),
            'enabled': True,
        }
    )