fruitex
=======

## Requirement

- Python 2.6 and above
- Pip

## Installation

```
pip install -r requirements.txt
python manage.py syncdb
# If creating a new db, use
python manage.py migrate
# If you have an existing up to date db, use
python manage.py migrate --fake
```
