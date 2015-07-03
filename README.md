# Pepperでニコ生コメントを読み上げる

Pepperアプリ開発ハッカソンで作成したものです．公開して大丈夫そうなので置いておきます．

参考(※) http://live.nicovideo.jp/watch/lv216923514

※超会議2015で使ったものとは．基本的には別物です

## 起動方法

- yomiage.pyに色々オプションがハードコードされてるので必要なものを書く必要がある．
- PC上で起動してPepperに接続する．(Pepper上でも動かせそうだが未確認)
- たぶん実機でなくてもChoregrapheのバーチャルロボットでも実行はできます．

```
python yomiage.py lvXXXXXXXXXXX email@example.com PASSWORD
```

メールアドレスに 'user_session' を指定し，パスワードとしてCookieから取得したuser_sessionを渡すことでブラウザ等と同じセッションを指定できます．

```
python yomiage.py lvXXXXXXXXXXX user_session user_session_00000000_xxxxxxxxxxxxxxxxxxx
```


## メモ

- nicolivecomment.py ニコ生コメントを取得するための汎用的なモジュールとして利用可能です
- pepper.py Pepperに喋らせたりxmlから読み込んだポーズを適用するモジュール


## License

MIT License.


