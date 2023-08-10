# dj-chat | A `django` and `htmx` chat application

Fully functional chat app built with `django` and `htmx` with the power of `websockets` and `channels`. The app also uses other production-level packages, such as:- channels, redis, django-allauth, django-crispy-forms, django-select2, etc.

> The main goal of this project is to show how django and htmx can be used to build a fully functional high quality application.
> Bootstrap5 is used to design the UI with custom styles.

![Screenshot 2023-08-10 155117](https://github.com/adilmohak/dj-chat/assets/60693922/db5c8628-36ef-446e-ae21-7d5f7a99adf5)

# Current features:

- **Private Messaging System:** Users can engage in private one-on-one chat conversations, known as threads.
- **Group Chat and Discussion Rooms:** The application supports group chat functionality, allowing users to participate in discussion rooms centered around specific topics.
- **User Authentication and Management:** Users can log in, log out, sign up, and manage(reset/change) their passwords.
- **Chat History Management:** Users can clear the chat history within a room, providing them with control over their chat environment.
- **Chat Deletion:** Users have the ability to delete entire chat conversations, offering a way to remove outdated or irrelevant discussions.
- **Sorting Options:** The discussions can be sorted based on trending topics, newest additions, or oldest discussions, enabling users to find relevant conversations efficiently.
- **Pagination and Infinite Scrolling:** The application utilizes pagination with infinite scrolling, allowing users to navigate through discussions seamlessly without page reloads. Messages inside private rooms are fetched automatically on the user scrolls up.
- **Recent Room Display:** Users can easily view their recent chat rooms, making it convenient to access frequently visited discussions.
- **Multicast Messaging:** Users can send messages to multiple recipients simultaneously.
- **Dynamic Room Creation and Update:** Users can create and update discussion rooms in real-time without the need to navigate away from the current page.
- **Real-time Discussion Search:** The application performs live discussion searches as users type, eliminating the need for page reloads and providing instant results.
- **Invitation Functionality:** Users can invite others to join a discussion room without interrupting their ongoing participation in the conversation.
- **Message Notifications:** Users have the option to mute or unmute message notifications, controlling their visibility and managing distractions.

# Pre-requisites:

> The following programs are required to run the project

- [Any Python-3 version](https://www.python.org/downloads/)
- [Redis](https://redis.io/download/)
- [PostgreSQL database](https://www.postgresql.org/download/)

# Installation

- First Clone the repo with `git clone https://github.com/adilmohak/dj-chat.git`

- Create and activate a python virtual environment

- `pip install -r requirements.txt`

- Create a `.env` file inside the root directory (Same directory where `manage.py` is located)

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

- `redis-server`

> The above command will start the redis server

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
