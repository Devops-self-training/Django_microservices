# Information before run

### Run check and run migration to admin and main

- Admin:
```bash
## best you need to exec to container admin to migrate
Python manage.py migrate
```
- Main:
```bash

## best you need to exec to container main to migrate and 
rm -rf ./migrations
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
``` 