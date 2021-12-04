# docker-compose exec app ./manage.py shell -c 'import event_to_csv'
from django.contrib.admin.models import LogEntry
from RadioActiv8.models import *
import csv

event_logs = LogEntry.objects.filter(content_type__app_label = "RadioActiv8", content_type__model = "event")

with open('log.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    header = ['Timestamp', 'Logging User', 'Patrol', 'Location', 'Comment']
    csvwriter.writerow(header)
    for e in Event.objects.all():
        e_log = event_logs.filter(object_id = e.id)[0]
        user = e_log.user.username

        #print(f'{e.timestamp},{user},{e.patrol},{e.location},{e.comment}')
        log_entry = [ e.timestamp, user, e.patrol, e.location, e.comment ]

        csvwriter.writerow(log_entry)
