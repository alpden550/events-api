# Events CRM

Events REST API based on Flask for crm, also includes admin panel.

[![Maintainability](https://api.codeclimate.com/v1/badges/7d9ada1345dd19a3aff1/maintainability)](https://codeclimate.com/github/alpden550/events-api/maintainability) [![Build Status](https://travis-ci.org/alpden550/events-api.svg?branch=master)](https://travis-ci.org/alpden550/events-api) [![Test Coverage](https://api.codeclimate.com/v1/badges/7d9ada1345dd19a3aff1/test_coverage)](https://codeclimate.com/github/alpden550/events-api/test_coverage) [![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## How to install

Download code or clone it from Github, and install dependencies.

If you have already installed Poetry, type command:

```bash
poetry install --no-dev
```

If not, should use a virtual environment for the best project isolation. Activate venv and install dependencies:

```bash
pip install -r requirements.txt
```

And set environment variables:

```bash
export SECRET_KEY=some extra secret key
```

## How to use

Before start, should initialize database and create superuser, if it needs.

```bash
flask init
flask superuser -n admin -p password -e test@mail.ru
```

And start web server:

```bash
flask run
```

## How to use API

* `GET /api/locations/` get all locations

* `GET /api/events/` get all events

* `GET /api/events?eventtype=hackaton` filter events by event type, use `event_type` from model

* `GET /api/events?location=москва` filter events by location

* `POST /api/enrollments/id=<eventid>` create enrollment for user, user pass in the body via json `{
   "email":"alpden@me.com"
   }`

* `DELETE /api/enrollments/id=<eventid>` delete enrollment for user, user pass in the body via json `{
   "email":"alpden@me.com"
   }`

* `POST /api/register` register user as participant.

  It needs required fields into passed json:

  `{
     "email":"test@gmail.com",
     "name": "Namу Surname",
     "password": "qwerty",
     "location": "Moscow",
     "about": "Some info about participant.."
  }`

* `POST /api/auth/` authorize participant
  It needs required fields into passed json:

  `{
     "email":"test@gmail.com",
     "password": "qwerty",
  }`

* `GET api/profile/id=<profileid>` get participant info.
