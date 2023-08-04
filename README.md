# dj-chat

### Fully functional chat app built with `django` and `htmx` with the power of `websockets`. The app includes other production level packages, such as:- channels, websockets, redis, django-allauth, django-crispy-forms, django-select2, etc.

# Current features:

- Threads / Private (one-on-one) chat
- Group chat / discussion rooms
- User management (Login/logout, signup, reset/change password)
- Mute/unmute message notifications
- Clear history
- Delete chat
- Sort discussions by "Trendings", "Newest", or "Oldest"
- Discussions pagination without page reloading
- Auto fetch messags onscroll
- Display the user's recent rooms

# Pre-requisites:

> The following programs are required to run the project, install them for your OS

- [Any Python-3 version](https://www.python.org/downloads/)
- [Redis](https://redis.io/download/)
- [PostgreSQL database](https://www.postgresql.org/download/)

# Installation

- First Clone the repo with `git clone https://github.com/adilmohak/dj-chat.git`

- Create and activate a python virtual environment

- `pip install -r requirements.txt`

- Create `.env` file inside the root directory (the same directory as where `manage.py` located)

- Inside your `.env` file put the following variables

```
DB_NAME=[NAME_OF_YOUR_DB]
DB_USER=[DB_USERNAME]
DB_PASSWORD=[DB_PASSWORD]
DB_HOST=localhost
DB_PORT=[DB_PORT]
```

- `python manage.py makemigrations`

- `python manage.py migrate`

- `python manage.py populate_data`

_The above command will populate sample data for you so you can test the app as quickly as possible_

- `redis-server`

_The above command will start the redis server_

- `python manage.py runserver`

- Last but not least, go to this address http://127.0.0.1:8000

# Connect with me

<div>
<a href="https://www.linkedin.com/in/adilmohak" target="_blank">
<img src=https://img.shields.io/badge/linkedin-%231E77B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white alt=linkedin style="margin-bottom: 5px;" />
</a>
<a href="https://github.com/adilmohak" target="_blank">
<img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</a>
<a href="https://stackoverflow.com/users/12872688/adil-mohak" target="_blank">
<img src=https://img.shields.io/badge/stackoverflow-%23F28032.svg?&style=for-the-badge&logo=stackoverflow&logoColor=white alt=stackoverflow style="margin-bottom: 5px;" />
</a>
<a href="https://www.facebook.com/adilmohak1" target="_blank">
<img src=https://img.shields.io/badge/facebook-%232E87FB.svg?&style=for-the-badge&logo=facebook&logoColor=white alt=facebook style="margin-bottom: 5px;" />
</a>
</div>

### Show your support by ⭐️ this project
