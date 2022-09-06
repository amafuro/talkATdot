# models.pyで登録したものをそのまま継承する

from django import forms
from django.contrib.auth.models import User
from .models import Account, Event


# フォームクラス作成
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    #クラスにform-controlを適用してBootstrapがデザインに適用できるようにする
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','password')
        # フィールド名指定
        labels = {'username':"ユーザーID",
                  'password':"パスワード",}

class AddAccountForm(forms.ModelForm):

    # クラスにform-controlを適用してBootstrapがデザインに適用できるようにする
    def __init__(self, *args, **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('nickname','university_name','campus_name','tweet',
                  'good_prog_language','bad_prog_language','account_image',)
        labels = {'nickname':"ニックネーム",
                  'university_name':"大学名",'campus_name':"キャンパス名",
                  'account_image':"写真アップロード",
                  'tweet':"ひとこと",
                  'good_prog_language':"得意な言語",
                  'bad_prog_language':"教えてほしい言語",
        }

class EventForm(forms.Form):
    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)
    event_name = forms.CharField(required=True, max_length=32)

class CalendarForm(forms.Form):
    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)