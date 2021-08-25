#!/usr/bin/env python
# coding: utf-8

import requests
import configparser
import base64
import json
import yaml
import datetime

Token_url = "https://libra.mdg.si.i.nagoya-u.ac.jp/oauth2/token"
Orion_url = "https://virgo.mdg.si.i.nagoya-u.ac.jp/v2/entities"

class mdgFiware:
  def __init__(self, id=None) -> None:
    with open('/setting.yaml', 'r') as yml:
      map = yaml.safe_load(yml)
      
      if id:
        self.__id = id
      else:
        self.__id = map['entity']['id']
        
      self.__type = map['entity']['type']
      self.__service = map['entity']['service']
      self.__servicepath = map['entity']['servicepath']
      self.__keys = map['keys']
      self.__cid = map['config']['client']['id']
      self.__cse = map['config']['client']['secret']
      self.__username = map['config']['user']['username']
      self.__password = map['config']['user']['password']
      self.__attrs = map['attributes']
      self.__ymlVersion = map['version']
      self.__token_url = Token_url
      self.__orion_url = Orion_url


  def showConfig(self) -> str:
    print("=== Config ===")
    print('id:\t\t', self.__id)
    print('type:\t\t',self.__type)
    print('service:\t',self.__service)
    print('servicepath:\t',self.__servicepath)
    print('token_url:\t',self.__token_url)
    print('orion_url:\t',self.__orion_url)


  def __getAuthToken(self) -> str:
    basic = base64.b64encode((self.__cid+":"+self.__cse).encode())
    headers_map = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": "Basic " + basic.decode(),
      "Accept": "application/json"
    }
    try:
      if self.__ymlVersion == 2:
        data = "grant_type=password" + "&username=" + self.__username + "&password=" + self.__password
        res = requests.post(self.__token_url, data=data, headers=headers_map)
        res.raise_for_status()
      else:
        raise Exception("setting.ymlのバージョンを確認してください。対応しているのは2のみです。")
    except Exception as e:
      raise
    else:
      return res.json()["access_token"]

  def sendData(self, raw, timestamp=None, console=True, debug=False) -> str:
    try: token = self.__getAuthToken()
    except Exception as e:
      print(e)
      print('トークンの取得中にエラーが発生しました。クライアントIDやクライアントシークレットを確認してください。')

    data = json.loads(raw)
    if timestamp == None:
      timestamp=datetime.datetime.utcnow()
    else:
      timestamp = timestamp[0:19]
      timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=-9)
    body = {
      'id': self.__id, 'type': self.__type,
    }
    body['dateObserved'] = {
      'type': 'DateTime',
      'value': timestamp.strftime('%Y-%m-%dT%H:%M:%S%Z'),
      'metadata': {}
    }
    if console: print("データをFIWAREに送信します...")
    try:
      for attr in self.__attrs:
        context = {
          'value': data[attr['value']],
          'type': attr['type']
        }
        body[attr['name']] = context
    except Exception as e:
      print(e)
      print('JSONのパース中にエラーが発生しました。設定ファイルの内容と引数のJSONの対応などを再確認してください。')  
    
    try:
      headers_map = {
        "Content-Type": "application/json",
        "X-Auth-Token": token,
        "Accept": "application/json",
        "fiware-service": self.__service,
        "fiware-servicepath": self.__servicepath
      }
      params_map = {
        "options": "upsert"
      }
      body = json.dumps(body)
      res = requests.post(self.__orion_url, data=body, headers=headers_map, params=params_map)
      res.raise_for_status()
    except Exception as e:
      print(e)
      print('FIWAREへのデータの送信中にエラーが発生しました。')
    else:
      if console: print("成功しました。")
      if debug: print(body)
      return res.status_code


  def getData(self, console=True) -> dict:
    token = self.__getAuthToken()
    if console: print("データをFIWAREから取得します...")
    try:
      headers_map = {
        "X-Auth-Token": token,
        "fiware-service": self.__service,
        "fiware-servicepath": self.__servicepath
      }
      res = requests.get(self.__orion_url, headers=headers_map)
      res.raise_for_status()
    except Exception as e:
      print(e)
      print('FIWAREからデータの取得中にエラーが発生しました。')
    else:
      if console: print("成功しました。データを表示します。")
      res = json.dumps(res.json(), indent=2)
      print(res)
      return res


if __name__ == '__main__':
  a = mdgFiware()
  a.show_config()
