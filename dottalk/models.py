"""
モデルを更新したらこの2つは必ずコンソールで行う
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
"""


from django.db import models
# ユーザー認証
from django.contrib.auth.models import User
#アカウント画像のファイル名の変更に使う
from django_cleanup import cleanup
import uuid

#アップロードされた画像の名前をuuidで作ったものに変更する
#元のファイル名からは拡張子のみを使うようにする
def image_directory_path(instance, filename):
    return 'profile_pics/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

# ユーザーアカウントのモデルクラス
# アカウント作成に必要なデータをまとめる
@cleanup.ignore
class Account(models.Model):

    # 1人1アカウントにする
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # アカウント作成日と更新日時
    posted_at = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)

    # 追加フィールド
    tweet = models.CharField(max_length=300)
    nickname = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    campus_name = models.CharField(max_length=100)
    good_prog_language = models.CharField(max_length=100)
    bad_prog_language = models.CharField(max_length=100)
    account_image = models.ImageField(upload_to="image_directory_path",blank=True)

    def __str__(self):
        return self.user

# コメント用
class Comment(models.Model):
    #コメント内容
    text = models.TextField(max_length=400)
    #コメント投稿者のアカウントニックネーム記録用
    posted_by = models.CharField(max_length=100)
    # コメント投稿者のアカウントid記録用
    posted_by_id = models.IntegerField()
    # コメント送信先のアカウントid記録用
    posted_to_id = models.IntegerField()
    # コメント投稿日時
    posted_at = models.DateTimeField(auto_now_add=True)
    #アカウントへのリレーション
    Account = models.ForeignKey(to=Account, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

#カレンダー用モデル
class Event(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event_name = models.CharField(max_length=200)

#アイデアモデル
class Idea(models.Model):

    title = models.CharField(max_length=128)
    text = models.TextField(max_length=400)
    posted_at = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)

    # コメント投稿者のアカウントニックネーム記録用
    posted_by = models.CharField(max_length=100)
    # コメント投稿者のアカウントid記録用
    posted_by_id = models.IntegerField()

    def __str__(self):
        return self.title

# コメント用
class Idea_comment(models.Model):
    #コメント内容
    text = models.TextField(max_length=400)
    #コメント投稿者のアカウントニックネーム記録用
    posted_by = models.CharField(max_length=100)
    # コメント投稿者のアカウントid記録用
    posted_by_id = models.IntegerField()
    # コメント送信先のアイデアid記録用
    posted_to_id = models.IntegerField()
    # コメント投稿日時
    posted_at = models.DateTimeField(auto_now_add=True)
    #アカウントへのリレーション
    Account = models.ForeignKey(to=Idea, related_name='idea_comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text