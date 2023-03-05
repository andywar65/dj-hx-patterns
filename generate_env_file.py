from pathlib import Path

from django.core.management.utils import get_random_secret_key

DIR = Path(__file__).resolve().parent

with open(Path(DIR / ".env"), "w") as f:
    f.write("SECRET_KEY=" + get_random_secret_key())
f.close()
