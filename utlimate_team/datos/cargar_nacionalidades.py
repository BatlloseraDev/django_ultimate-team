import os
import django
import pandas as pd
from django.conf import settings
from ..ultimate_team_app.models import Nacionalidad


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ultimate_team.settings")
django.setup()

# Lee el archivo
archivo = os.path.join(settings.BASE_DIR, "datos", "paisesyterritorios.xlsx")
df = pd.read_excel(archivo)

# Guardar nacionalidades en la base de datos (Los países están en la columna 5)
for nombre in df.iloc[:, 5]:
    if isinstance(nombre, str) and nombre.strip():
        Nacionalidad.objects.get_or_create(nombre=nombre.strip())




