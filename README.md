# RadioActiv8

This is a Django app (as opposed to a project) designed to model the RadioActiv8 activity.

## Getting started

Add this to a GeoDjango project.

## Load test data

Test data lives in the `test_data.py` file.
```sh
docker-compose exec web python manage.py shell -c 'from RadioActiv8 import test_data; test_data.load()'
```
