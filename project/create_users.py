from django.contrib.auth.models import User

users = ["Laura", "Carolina", "Margarida"]

def create_sample_users():
    for name in users:
        mail = name.lower() + "@iscte.pt"
        password = "12345"
        User.objects.create_user(name, mail, password)

create_sample_users()