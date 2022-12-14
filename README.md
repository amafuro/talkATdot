# [talkATdot](https://talkatdot.herokuapp.com/)
農学専攻の自分の周りにはプログラミングをやっている人はポツポツいます。しかし全員情報交換をする機会も無いので孤独にやっている人が多いなと感じていました。
またプログラミングをやってみたいけど、なんか難しそうだし手を出せない。といった人もかなり多いとも感じていました。

そこで同じ大学・同じキャンパスという物理的距離が近く、プログラミングに興味のある人達が繋がることができれば、互いに教え合ったりすることが簡単になるのではないかと思い、このアプリの制作に至りました。

また全ユーザーが情報をシェアする機能（シェアカレンダー、アイデアの森）をつけることで、学生にとって有益なプログラミング関連の情報を効率的に集められるようにしました。

## ポイント
- 全般
  - 情報系の学部じゃない場合でもデータ解析などで使われていることが多いPython（3.10.7）を使用。
    狙いとしては、普段なじんでいる（もしくは聞いたことのある）プログラミング言語でこのアプリを作成することで、初心者の方のwebアプリ作成のハードルを下げれたらいいなと思ってます。
  - フレームワークとしてDjango（4.1）とBootstrap（4.3.1と5.0.2）を使用
  - BootstrapとFullCalendarはCDNで利用
  - ユーザーは大学生でプログラミング初心者～中級者を想定
  
- HOME（Same campus users）
  - 同じ大学・キャンパス名で登録したアカウントを一覧表示
  - 更新があったユーザーを左上に配置
  - ページ下部の検索フォームからアカウントを検索できる
  
- talkroom
  - HOMEでクリックしたアカウントへのコメント一覧を表示する
  - ヘッダーとフッターをクリックすることでページの上下の移動をできるようにした
  - フッターに部屋主の「得意言語・勉強中の言語・ひとこと」を常に表示するように設定
  
- My page（マイページ）
  - 画面上部に自分のアカウントの情報の更新部分、下部に自分宛に届いたコメント表示
  - アカウント削除ボタンを押すと最終確認のモーダルが表示
  
- Footprint（あしあと）
  - 自身がコメントを送ったアカウントを表示

- Calendar（シェアカレンダー）
  - 全アカウント共通のカレンダーを表示。FullCalendar（5.11.3）を使用
  - イベント一覧ページではアクセス当日から3週間以内に始まるイベントを表示
    - 編集ボタンから予定の編集・削除ができるようにした。
    - 検索フォームから過去のイベントを含め、イベントの検索をできるようにした。
  - [x] 自分の所属している研究室ではGoogleカレンダーで全員の予定を管理しています。同期の公開しているカレンダーイベントを見て、面白そうなイベントを知ったり、課題の締め切りを思い出して助かった経験をしました。これをもっと多くの人の規模でやれたら、様々な企業イベントや就活イベントを網羅した、最強のカレンダーができるのじゃないかと思い作成に至りました。
  
- Idea forest（アイデアの森）
  - 何かプログラミングで作りたくなったときに、全アカウントに向けてアイデアを募集するページ
  - 各投稿をクリックすることで詳細を表示。コメントを投稿できる。
  - 各投稿は投稿したアカウントのみ削除ができる。（投稿したアカウントのみ削除ボタンをアクティベートする）
  - フッターから自分の投稿のみを表示したり、検索フォームから目的の投稿を探せるようにした。
  - [x] 以前自分がなにかプログラミングでモノを作ってみたいと考えていたときに、なかなかいいアイデアが出ずに困っていたことがありました。このアプリは大学生のユーザーを想定しており、年齢の近い人からの意見がもらいやすいと考えました。そこでアイデアやそれに対するフィードバックがもらえる場を設けることで、学生の制作活動に助けられるのではないかと思い制作しました。
  
