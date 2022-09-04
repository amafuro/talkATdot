from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.Login,name="Login"),
    path("logout",views.Logout,name="Logout"),
    # クラスベースの場合は as_view メソッドを呼び出す
    path("register",views.AccountRegistration.as_view(), name="register"),
    path("same_users_all",views.same_campus_users.as_view(),name="same_users_all"),
    #idは各アカウントの主キー
    path("talkroom/<int:id>/",views.talkroom,name="talkroom"),
    #お問い合わせ先ページ
    path("infomation",views.infomation,name="infomation"),
    #アカウントの編集ページ
    path("edit",views.edit,name="edit"),
    #アカウント削除リンク
    path("edit/delete/",views.delete,name="delete"),
    #あしあと表示用
    path("footprint",views.footprint.as_view(),name="footprint"),
]
#アカウント画像を表示する際にURLを反映する
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)