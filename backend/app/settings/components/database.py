from pathlib import Path
import os

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     os.getenv("POSTGRES_DB",       "mydb"),
        "USER":     os.getenv("POSTGRES_USER",     "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST":     os.getenv("POSTGRES_HOST",     "database"),
        "PORT":     os.getenv("POSTGRES_PORT",     "5432"),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIUM_FIELD_LENGTH = 255

