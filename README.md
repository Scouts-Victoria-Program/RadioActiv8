# RadioActiv8

This is a Django project designed to model the RadioActiv8 activity.

## Getting started

1. Clone this repo, cd into it, and copy the `.env` file:

```sh
git clone https://github.com/Radio-Active-Scout/RadioActiv8
cd RadioActiv8
cp .env.example .env
```

2. Start up the Docker environment:

```
docker-compose up -d
```

3. Load in some test data (stored in `test_data.py`)

```
docker-compose exec app python manage.py shell -c 'from RadioActiv8 import test_data; test_data.load()'
```

4. Log into http://localhost:8000/admin as `root`/`root`, and explore the data.
