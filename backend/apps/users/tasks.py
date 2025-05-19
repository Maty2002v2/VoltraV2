import requests
from celery import shared_task
from django.conf import settings
from apps.users.models.user import UserProfile
from django.contrib.auth.models import User

OKAYCRM_API_KEY = "9ebd0453a8aba6d8d2f73a084a94f4a87477c306"
OKAYCRM_PERSONS_URL = "https://voltratest.okaycrm.com/api/v2/persons/"

@shared_task
def sync_users_from_okaycrm():
    profiles = UserProfile.objects.exclude(okaycrm_id__isnull=True).exclude(okaycrm_id__exact='')

    for profile in profiles:
        try:
            response = requests.get(
                f"{OKAYCRM_PERSONS_URL}{profile.okaycrm_id}/",
                headers={"Api-Key": OKAYCRM_API_KEY}
            )
            if response.status_code == 200:
                data = response.json().get("data")

                if not data:
                    continue

                user = profile.user

                # porównujemy i aktualizujemy dane
                updated = False
                if user.first_name != data.get("imie"):
                    user.first_name = data["imie"]
                    updated = True
                if user.last_name != data.get("nazwisko"):
                    user.last_name = data["nazwisko"]
                    updated = True
                if user.email != data.get("email"):
                    user.email = data["email"]
                    updated = True
                if profile.phone_number != data.get("telefon"):
                    profile.phone_number = data["telefon"]
                    updated = True

                if updated:
                    user.save()
                    profile.save()

            else:
                print(f"❌ Błąd przy pobieraniu użytkownika OkayCRM {profile.okaycrm_id}: {response.status_code}")

        except Exception as e:
            print(f"❌ Błąd synchronizacji użytkownika {profile.okaycrm_id}: {e}")
