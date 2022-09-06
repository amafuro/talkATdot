from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from . import models
# テンプレートタグ
from django.views.generic import TemplateView, ListView
# ユーザーアカウントフォーム
from .forms import AccountForm, AddAccountForm
# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# トークルーム指定時に対象のアカウントがなければ404
from django.http import Http404
#検索フォーム用
from django.db.models import Q
#カレンダー
import json
from .models import Event
from .forms import EventForm
import time
from django.http import JsonResponse
from .forms import CalendarForm

#アカウントを登録する際のクラスビュー
class  AccountRegistration(TemplateView):
    #ユーザーがアカウントを作ろうとしたとき、問題が無いか判断する為にAccountCreateを作成
    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    # Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"HTML/register.html",context=self.params)

    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # フォーム入力に問題が無いか検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をデータベースに保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 追加情報について
            # 下のコードを動かすためにコミットしない
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"HTML/register.html",context=self.params)


#ログインする際の関数ビュー
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse("same_users_all"))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")

        else:
            # ユーザー認証失敗
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'HTML/login.html')


#ログアウト
#@マークをつけることでログイン中のみ遷移可能にする
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))

#アカウントの新規登録
class AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    #Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"HTML/register.html",context=self.params)

    #Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        #フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"HTML/register.html",context=self.params)


# 自分の大学・キャンパスが一致するアカウントを検索、クエリーセットとする
# 検索ワードがあった場合はそれを含めて検索
class same_campus_users(ListView,LoginRequiredMixin):
    model = models.Account
    template_name = "HTML/same_users_all.html"
    def get_queryset(self):
        # ログイン中のユーザーのクエリーセットを取得
        loginuser_uni = models.Account.objects.get(user=self.request.user)
        #検索ワードを取得
        q_word = self.request.GET.get('query')
        if loginuser_uni is None:
            return redirect("Login")

        # 大学、キャンパス、気になる言語（検索ワード）が一致するものを取得
        if q_word :
            object_list = models.Account.objects.filter(
                # Qオブジェクトのandは&,orは|、自分のアカウントを除き、新しい順にする
                Q(university_name=loginuser_uni.university_name)&
                Q(campus_name=loginuser_uni.campus_name)&
                Q(nickname__icontains=q_word) |
                Q(good_prog_language__icontains=q_word) |
                Q(bad_prog_language__icontains=q_word)).exclude(user=self.request.user).order_by('-last_modify')
        #検索ワードがなければ大学、キャンパスが一致するものを取得
        else:
            object_list = models.Account.objects.filter(
                university_name=loginuser_uni.university_name,
                campus_name=loginuser_uni.campus_name).exclude(user=self.request.user).order_by('-last_modify')
        return object_list


#各アカウントのトークルーム
def talkroom(request,id):
    template_name = "HTML/talkroom.html"
    try:
        #選択されたアカウントの情報を取得する
        Account = models.Account.objects.get(id=id)
    except models.Account.DoesNotExist:
        #選択されたアカウントがなければ404を返す
        raise Http404
    if request.method == "POST":
        # コメント投稿者のアカウント取得
        loginuser = models.Account.objects.get(user=request.user)
        # データベースに投稿されたコメント、投稿者名を保存
        models.Comment.objects.create(text=request.POST["text"],
                                      posted_by=loginuser.nickname,
                                      posted_by_id=loginuser.id,
                                      posted_to_id=Account.id,
                                      Account=Account)
        # コメントが投稿されたら、投稿されたアカウントの方の更新日も更新する
        Account.save()
    context = {"Account":Account}
    return render(request,template_name,context)

#お問い合わせ先を表示
def infomation(request):
    return render(request, "HTML/infomation.html")

#マイページを編集
@login_required
def edit(request):
    template_name = "HTML/edit.html"
    try:
        Account = models.Account.objects.get(id=request.user.id)
    except models.Account.DoesNotExist:
        raise Http404
    if request.method == "POST":
        if "btn_comment" in request.POST:
            # コメント投稿者のアカウント取得
            loginuser = models.Account.objects.get(user=request.user)
            # データベースに投稿されたコメント、投稿者名を保存
            models.Comment.objects.create(text=request.POST["text"],
                                          posted_by=loginuser.nickname,
                                          posted_by_id=loginuser.id,
                                          posted_to_id=Account.id,
                                          Account=Account)
            # コメントが投稿されたら、投稿されたアカウントの方の更新日も更新する
            Account.save()
            return redirect("edit")
        else :
            # フォーム入力の有効検証
            if AddAccountForm(request.POST).is_valid():
                Account.nickname = request.POST["nickname"]
                Account.university_name = request.POST["university_name"]
                Account.campus_name = request.POST["campus_name"]
                Account.tweet = request.POST["tweet"]
                Account.good_prog_language = request.POST["good_prog_language"]
                Account.bad_prog_language = request.POST["bad_prog_language"]
                Account.save()
                return redirect("same_users_all")
            else:
                # フォームが有効でない場合
                print(AddAccountForm(request.POST).errors)
    context = {"Account": Account}
    return render(request, template_name, context)

#アカウントを削除する
@login_required
def delete(request):
    try:
        #ログインしているユーザーのUserモデルを削除
        #付随するAccountモデル・Commentモデル(マイページにあるもの)も削除される
        models.User.objects.filter(id=request.user.id).delete()
    except models.Account.DoesNotExist:
        raise Http404
    return HttpResponseRedirect(reverse('Login'))

#履歴を表示する
class footprint(ListView,LoginRequiredMixin):
    model = models.Account
    template_name = "HTML/footprint.html"
    def get_queryset(self):
        #ログイン中のアカウント情報を取得
        loginuser = models.Account.objects.get(user=self.request.user)
        # ログイン中のユーザidと一致するコメントを取得
        fp = models.Comment.objects.filter(Q(posted_by_id=loginuser.id)).values_list('posted_to_id', flat=True)
        # 取得したコメント先アカウントのidをリストにする
        fp_list = list(fp)
        print(fp_list)
        #　コメント先アカウント一覧を取得、最後にコメントしたものが一番上になるように並び替えるlast_modify
        #自分のアカウントは表示しないようにする-comments__posted_at
        object_list = models.Account.objects.filter(Q(id__in=fp_list)).order_by('-last_modify')
        return object_list

#カレンダー
@login_required
def calendar(request):
    template_name = "HTML/calendar.html"
    return render(request, template_name)
@login_required
def add_event(request):
    """
    イベント登録
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    eventForm = EventForm(datas)
    if eventForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # 登録処理
    event = Event(
        event_name=str(event_name),
        start_date=formatted_start_date,
        end_date=formatted_end_date,
    )
    event.save()

    # 空を返却
    return HttpResponse("")
@login_required
def get_events(request):
    """
    イベントの取得
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    calendarForm = CalendarForm(datas)
    if calendarForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # FullCalendarの表示範囲のみ表示
    events = Event.objects.filter(
        start_date__lt=formatted_end_date, end_date__gt=formatted_start_date
    )

    # fullcalendarのため配列で返却
    list = []
    for event in events:
        list.append(
            {
                "title": event.event_name,
                "start": event.start_date,
                "end": event.end_date,
            }
        )

    return JsonResponse(list, safe=False)