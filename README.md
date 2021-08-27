# po8klasie API

## Local development

Requirements:
- docker
- docker-compose

### Install requirements
```shell script
pip install -r requirements.txt
```

### Run
```shell script
docker-compose up -d --build # build and start db container
python manage.py migrate
python manage.py runserver 8000
```

The application should be available at `127.0.0.1:80`.

#### Linter
We use [black](https://github.com/psf/black) autoformatter and flake8. 

Run:
```shell script
black .
flake8
```
