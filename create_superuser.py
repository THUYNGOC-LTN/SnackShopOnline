from django.contrib.auth import get_user_model

User = get_user_model()

username = "adminngoc"
password = "123456"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        password=password,
        email="admin@gmail.com"
    )
    print("Superuser created")
else:
    print("Superuser already exists")