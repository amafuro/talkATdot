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
    path("edit/",views.edit,name="edit"),
    #アカウント削除リンク
    path("edit/delete/",views.delete,name="delete"),
    #あしあと表示用
    path("footprint",views.footprint.as_view(),name="footprint"),
    #カレンダー表示、追加
    path("calendar",views.calendar,name="calendar"),
    path("add/", views.add_event, name="add_event"),
    path("list/", views.get_events, name="get_events"),
    #カレンダーイベント一覧表示、削除
    path("calendar/event_list/",views.calendar_event_list.as_view(),name="event_list"),
    path("event_edit/<int:id>/",views.event_edit,name="event_edit"),
    path("event_edit/<int:id>/delete/",views.event_delete,name="event_delete"),
    #アイデア出し詳細ページ
    path("idea_detail/<int:id>/",views.idea_detail,name="idea_detail"),
    #アイデア投稿ページ
    path("idea_new/",views.idea_new, name="idea_new"),
    #アイデア一覧
    path("idea_list/",views.idea_list.as_view(),name="idea_list"),
    #アイデア削除用
    path("idea_delete/<int:id>/",views.idea_delete,name="idea_delete"),
]
#アカウント画像を表示する際にURLを反映する
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)