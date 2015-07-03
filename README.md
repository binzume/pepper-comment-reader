# Pepperでニコ生コメントを読み上げる

Pepperアプリ開発ハッカソンで作成したものです．

## 起動方法

- yomiage.pyに色々オプションがハードコードされてるので必要なものを書く必要がある．
- PC上で起動してPepperに接続する．(Pepper上でも動かせそうだが未確認)

```
python yomiage.py lvXXXXXXXXXXX email@example.com PASSWORD
```

メールアドレスに 'user_session' を指定し，パスワードとしてCookieから取得したuser_sessionを渡すことでブラウザ等と同じセッションを指定できます．

```
python yomiage.py lvXXXXXXXXXXX user_session user_session_00000000_xxxxxxxxxxxxxxxxxxx
```

