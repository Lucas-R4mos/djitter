from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    published_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def timestamp(self):
        import datetime

        timestamp = datetime.datetime.now() - self.published_at

        if timestamp.days == 0:
            if timestamp.seconds <= 60:
                return 'Agora'

            elif timestamp.seconds <= 3600:
                return f'{int(timestamp.seconds/60)} m'

            else:
                return f'{int(timestamp.seconds/3600)} h'

        else:
            return f'{timestamp.days} d'

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=140, default='')
