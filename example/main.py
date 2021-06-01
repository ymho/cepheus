import cepheus
import json

m1 = cepheus.mdgFiware()
data = {
  'people': {'right': 0, 'left': 0},
  'car': {'right': 64, 'left': 46},
  'truck': {'right': 150, 'left': 55},
  'bus': {'right': 23, 'left': 23},
  'motorcycle': {'right': 15, 'left': 1},
}
m1.showConfig()
m1.sendData(json.dumps(data), '2021-05-10 14:08:00.016578+09:00') #タイムスタンプは省略可能
m1.getData()  # 最新のデータを閲覧