from django.contrib import admin

# Register your models here.
from .models import AddNews,Comment

admin.site.register(AddNews)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'content', 'posted_at')  # 管理画面に表示するフィールドを指定
    search_fields = ('user__username', 'content')  # 検索フィールドを指定

admin.site.register(Comment, CommentAdmin)  # Commentモデルを登録
