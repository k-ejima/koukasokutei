from django.db import models
from django.conf import settings
# Create your models here.
class AddNews(models.Model):
    CATEGORY = (('government','政治,経済'),
                ('entertainment','エンターテインメント'),
                ('sports','スポーツ'),
                )
    
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )

    content = models.TextField(
        verbose_name='本文'
    )

    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    category = models.CharField(
        verbose_name='ジャンル',
        max_length=50,
        choices=CATEGORY
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(AddNews, on_delete=models.CASCADE, related_name='comments')  # ニュース記事への外部キー
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ユーザーへの外部キー
    content = models.TextField(verbose_name='コメント')  # コメント内容
    posted_at = models.DateTimeField(auto_now_add=True)  # コメントの投稿日時

    def __str__(self):
        # コメントの内容を20文字まで表示
        return f'{self.user.username} - {self.content[:20]}'