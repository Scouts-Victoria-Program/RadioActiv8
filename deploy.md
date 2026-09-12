# Guide to deploying RadioActiv8 for field use

> [!IMPORTANT]
> The following presumes a clean version of a Debian-based system ready for RadioActiv8 deployment. This has been tested using a Debian 12 `arm64` image. This *should* also work on `amd64` systems. Use at your own ~peril~ discretion.

Do the doing of the things:


## Install Docker core
``` sh
sudo apt update
sudo apt install docker.io -y		# Install docker.io
sudo systemctl status docker 		# Check that it's doing the thing - green is good
sudo adduser <username> docker		# Add local user to the docker group
logout					# Logout
```

### Test that docker runs using hello-world
``` sh
ssh <username>@<debian-machine>		# Log back in again
docker run --rm hello-world		# Start the test container
```

### Install docker-compose functionality

``` sh
sudo mkdir -p /usr/local/libexec/docker/cli-plugins/
sudo curl -L https://github.com/docker/compose/releases/download/v2.27.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/libexec/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/libexec/docker/cli-plugins/docker-compose
```

## Install RadioActiv8

#### Clone RadioActiv8 into a directory and set the environment variables

``` sh
cd <container directory (/srv/, /opt/, whatever)>
git clone https://github.com/Scouts-Victoria-Program/RadioActiv8
cd RadioActiv8/

# OPTIONAL: If you want to not specify the `-f` flag...
cp docker-compose.prod.yml docker-compose.yml

# Create custom environment variables for your install (default :8000)
cp .env.example .env
```

####  Initialize your container
``` sh
docker compose up -d && docker compose logs -f
```

Wait indefinitely for everything to download and run successfully.
> Ignore the WARN[0000] .../RadioActiv8/docker-compose.yml: \`version\` is obsolete

`Running on http://<hostname>:8000...`

## Cleanup, smoothing, and sample data

### Fixing the CSRF error when logging into `http://<hostname>/admin` as default `root/root`

Change this line:

`CSRF_TRUSTED_ORIGINS=http://localhost:$APP_PORT`

To this:

`CSRF_TRUSTED_ORIGINS=http://localhost:$APP_PORT,http://<hostname>:$APP_PORT`

Then, restart the container to execute changes

```sh
docker compose up -d && docker compose logs -f
```

In your browser, navigate to `http://<hostname>:8000/admin`
Login with default credentials `root/root`.

### Load Sample Data

Load the sample data into the installation (if you wish to play around)

``` sh
docker compose exec app ./manage.py loaddata sample
# Ignore the following warning:
# ?: (staticfiles.W004) The directory '/code/static' in the STATICFILES_DIRS setting does not exist.
```

## Importing a bases and intelligences CSV

#### Create a CSV called `bases.csv` with three columns: "base", "question", "answer", for example:
```csv
base,question,answer
Banana,What is your favourite colour?,yellow
Banana,What is your name?,Larry
Apple,What is the airspeed of unlaiden swallow?,African
```
For readability assistance:
| base   | question                                  | answer  |
| ------ | ----------------------------------------- | ------- |
| Banana | What is your favourite colour?            | yellow  |
| Banana | What is your name?                        | Larry   |
| Apple  | What is the airspeed of unlaiden swallow? | African |

#### Copy the CSV into the Docker container: `docker compose cp bases.csv app:/code`

#### Start an interactive Python shell in the container: `docker compose exec app ./manage.py shell_plus`

#### Run the following code:
```python
import csv
from RadioActiv8.models import Base, Intelligence, Session
# Replace "DEFAULT SESSION" below with your session name, if applicable
session = Session.objects.get(name="DEFAULT SESSION")
with open("bases.csv") as f:
reader = csv.DictReader(f)
for row in reader:
    base, status = Base.objects.get_or_create(
        name=row["base"],
        description=row["base"],
        )
    base.session.add(session)
    intelligence = Intelligence.objects.get_or_create(
        base=base,
        question=row["question"],
        answer=row["answer"],
        )
```

```exit()``` the Python shell.

## Importing Patrols to a Session

The same concept for Bases and Intelligence can be done for Patrols. These are normally numbers for RadioActiv8 but the example below will use names.

#### Create a CSV called `patrols.csv` with two columns: "name", "pax" (people). For example:

```csv
name,pax
platypus,6
koala,4
kangaroo,5
quokka,7
```

For readability assistance:
| name     | pax |
| -------- | --- |
| platypus | 6   |
| koala    | 4   |
| kangaroo | 5   |
| quokka   | 7   |

#### Copy the CSV into the Docker container: `docker compose cp patrols.csv app:/code`

#### Start an interactive Python shell in the container: `docker compose exec app ./manage.py shell_plus`

```python
import csv
from RadioActiv8.models import Patrol, Session
# Replace "DEFAULT SESSION" below with your session name, if applicable
session = Session.objects.get(name="DEFAULT SESSION")
with open("patrols.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        patrol, status = Patrol.objects.get_or_create(
            name=row["name"],
            number_of_members=row["pax"],
            )
        patrol.session.add(session)
```

```exit()``` the Python shell.

~~ EOF ~~
