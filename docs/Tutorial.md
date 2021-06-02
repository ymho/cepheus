# チュートリアル

使い方の例を下記に示します。この内容のソースコードは`example`フォルダーにあります。
なお，このドキュメントはブランチごとに最適な値になるようにあらかじめ指定されています。

## #1 モジュールのインポート
```python
import cepheus
```

## #2 インスタンスの生成

まず，`mdgFiware()`でインスタンスを生成します。**引数として，`id`を含めることができます。引数に`id`を指定すると`setting.yaml`に設定した`id`が上書きされます。これは，同一スクリプト内で複数のコンテキストを扱う場合に便利です。**
```python
m1 = cepheus.mdgFiware()  #setting.yamlに従う場合
m1 = cepheus.mdgFiware(id='<id>') # idを手動で設定する場合
```
この時点で，FIWAREに送信に必要なパラメータがコンストラクタとして登録されています。確認したい場合は
```python
m1.showConfig()
```
として確認できます。

## #3 `setting.yaml`の設定

andoromedaを使うには，あらかじめ`setting.yaml`を適正に設定して，**andoromedaを呼び出すPythonスクリプトと同じ階層に設置**する必要があります。下記のようなディレクトリ構成にしてください。

```
.
├── main.py
└── setting.yaml
```

### #3-1 設定例

cepheusより`version`が2に更新されています。`1`だとエラーが出ます。

```yaml
version: 2

config:
  client:
    id: client_id
    secret: client_secret
  user:
    username: user@mdg.com
    password: password

keys:
  - people
  - car
  - truck
  - bus
  - motorcycle

entity:
  id: jp.nagoya-u.mdg.gifu.takayama.traffic.dev001
  type: Traffic
  service: traffic
  servicepath: /gifu/takayama

# nameは一度決めたら変更しないでください
# valueはプログラム内で扱うJSONデータのkeyを設定してください

attributes:
  - name: people
    type: json_array
    value: people
  - name: car
    type: json_array
    value: car
  - name: truck
    type: json_array
    value: truck
  - name: bus
    type: json_array
    value: bus
  - name: motorcycle
    type: json_array
    value: motorcycle
```

下記で順次解説します。

### #3-2 ユーザー登録

~~`username`と`password`は下記のフォームから申請してください。~~

**現在登録は手動でやっているので個別にご連絡ください。**

<!-- [登録フォーム](https://forms.office.com/r/XZqYeYhnBg) -->

~~申請には名古屋大学のMicrosoftアカウントが必要です。パスワードは全学メールアドレスのものと同じですが，メールアドレスの表記が異なります。下記は[名古屋大学のホームページ](https://icts.nagoya-u.ac.jp/ja/services/office365/)からの抜粋です。これを参考にログインして申請してください。~~

> ~~全学メールアドレスが nagoya.hanako@b.mbox.nagoya-u.ac.jpの場合、Office 365アドレスは nagoya.hanako@b0.nagoya-u.jpとなります。~~

なお，上記の例では，以下のクライアントIDとクライアントシークレット，ユーザーネームとパスワードが取得できたと仮定しています。

| 種別 | 値 |
|:----:|:----:| 
| client id | id000000-XXXX-XXXX-XXXX-XXXXXXXXXXXX |
| client_secret | secret00-XXXX-XXXX-XXXX-XXXXXXXXXXXX |
| usename | user@mdg.com |
| password | password |

これらの値を`seting.yaml`に登録してください。
```yaml
config:
  client:
    id: id000000-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    secret: secret00-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  user:
    username: user@mdg.com
    password: password
```

### #3-3 `keys`の設定

`setting.yaml`で`keys`を設定します。ここに設定するのは，**Pythonスクリプトで生成されるJSONのkey**です。設定例では，下記のようなJSONを想定しています。
```json
{
  "people": {"right": 0, "left": 0},
  "car": {"right": 64, "left": 46},
  "truck": {"right": 150, "left": 55},
  "bus": {"right": 23, "left": 23},
  "motorcycle": {"right": 15, "left": 1},
}
```

### #3-4 `entity`の設定
`setting.yaml`で`entity`を設定します。必要なのは下記の値です。

| パラメータ  | 値（例） |
|:----:|:----:| 
| id | jp.nagoya-u.mdg.gifu.takayama.traffic.dev001 |
| type | Traffic |
| fiware-service | traffic |
| fiware-servicepath | /gifu/takayama |

`id`はコンテキストを一意に定める識別子ですので，**重複することはできません**。下記

* `jp.nagoya-u.mdg.gifu.takayama.traffic.dev001`
* `jp.nagoya-u.mdg.gifu.takayama.traffic.dev002`
* ...

のように，設置するデバイスごとに`setting.yaml`を編集して指定してください。**`fiware-service`や`fiware-servicepath`はそのまま**にしてください。

### #3-5 `attributes`の設定

`setting.yaml`で`attributes`を設定します。これは，JSONの値とfiwareでの値の対応付けに関する設定です。`name`がfiwareでのアトリビュートで`value`がJSONのkeyです。原則として`name`と`value`は同じ値にします。

なお，`setting.yaml`の`keys`に登録したものは必ず`attributes`の`value`に含まれている必要があります。

以上で`setting.yaml`の設定は終わりです。

## #4 データの送信

それでは，実際にPythonスクリプト内でデータを送信しましょう。
まずJSONのもとになる`data`を用意するようお願いします。

それをJSONにdumpしたものを，`sendData`メソッドの第1引数として与えてください。これは，必須パラメータです。

また，必要であれば第2引数としてタイムスタンプを与えてください。**タイムスタンプは必須パラメータではありません。** 指定しない場合，`sendData`メソッドは実行されたタイミングで自動でタイムスタンプを付加します。

```python
data = {
  'people': {'right': 0, 'left': 0},
  'car': {'right': 64, 'left': 46},
  'truck': {'right': 150, 'left': 55},
  'bus': {'right': 23, 'left': 23},
  'motorcycle': {'right': 15, 'left': 1},
}
m1.sendData(json.dumps(data), '2021-05-10 14:08:00.016578+09:00')
```

データを送信すると，コンソールに下記のように表示されます。
```bash
データをFIWAREに送信します...
成功しました。
```

エラーが発生した場合，その旨が表示されますが，対応しきれいていない部分もあるかもしれません。その際は，issueやコンタクトをください。

## #5 まとめ

以上のPythonスクリプトをまとめると下記のようになります。
```python
import cepheus
import json

m1 = cepheus.mdgFiware(id='jp.nagoya-u.mdg.gifu.takayama.traffic.dev001')
data = {
  'people': {'right': 0, 'left': 0},
  'car': {'right': 64, 'left': 46},
  'truck': {'right': 150,'left': 55},
  'bus': {'right': 23, 'left': 23},
  'motorcycle': {'right': 15, 'left': 1},
}
m1.sendData(json.dumps(data), '2021-05-10 14:08:00.016578+09:00') #タイムスタンプありの場合
m1.sendData(json.dumps(data)) #タイムスタンプなしの場合
m1.getData()  # 最新のデータを閲覧
```