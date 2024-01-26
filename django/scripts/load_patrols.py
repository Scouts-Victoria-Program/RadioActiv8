# docker compose exec app ./manage.py shell -c 'import load_patrols'
from RadioActiv8.models import *

with open("patrols.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    p = Patrol(name=line.strip())
    p.save()
