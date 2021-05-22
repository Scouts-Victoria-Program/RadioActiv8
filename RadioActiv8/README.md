# RadioActiv8

This is a Django app (as opposed to a project) designed to model the RadioActiv8 activity.

## Getting started

1. Clone @mattcen's Dockerised GeoDjango repo, cd into it, and copy the `.env` file:

```sh
git clone -b geodjango https://github.com/mattcen/geodjango_tutorial mydjango
cd mydjango
cp .env.example .env
```

2. Clone this repo:

```
git clone https://github.com/Radio-Active-Scout/RadioActiv8
```

3. Add `RadioActiv8` to the `INSTALLED_APPS` section of `geodjango/settings.py`.

4. Start up the Docker environment:

```
docker-compose up -d
```

5. Load in some test data (stored in `test_data.py`)

```
docker-compose exec web python manage.py shell -c 'from RadioActiv8 import test_data; test_data.load()'
```

5. Log into http://localhost:8000/admin as `root`/`root`, and explore the data.
