# cepheus

## 用途
JSONをNGSIに整形してmdgのFIWAREにPOSTするツールです。JSONとNGSIの対応は`settings.yaml`に登録してください。
* andoromedaの後継版です。

## 使い方
### インストール
`pip`コマンドでインストールできます。`pip3`であれば下記のように実行します。

```bash
pip3 install -U git+https://github.com/mdg-nu/cepheus.git@ブランチ名
```

### もっともはやい手順

#### #1 `setting.yaml`の設定
取得した`client_id`，`client_secret`，`username`，`password`を`setting.yaml`に記入します。

#### #2 スクリプトによる実装

Pythonスクリプトの冒頭に
```python
import cepheus
```
と記述します。これでモジュール群が使えるようになります。さらなる使い方は[チュートリアル](./docs/Tutorial.md)をご覧ください。

## トラブル・改善
問題がございましたら`issue`にお願いします。