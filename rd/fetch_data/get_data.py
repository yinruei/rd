import pandas as pd
import numpy as np
import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
import env

from django.conf import settings

def get_green_restaurant_data():
    green_restaurant = []
    df = pd.read_excel(os.path.join(settings.DATA_ROOT, "map_data.xlsx"), sheet_name="A綠餐廳蔬食")
    header = ['店名', '地址(A-格式不限)', '經度', '緯度', '電話', '開放時間(統一格式)',
            '照片0__(fb目前頭貼)', '照片1','照片2', '照片3', '照片4', '照片5', '照片6',
            '照片(推薦頁)','近期更新時間']

    filter_header_data = df[header]
    data = filter_header_data.replace(np.nan, '', regex=True)

    img_ch_list = ['照片0__(fb目前頭貼)', '照片1', '照片2', '照片3', '照片4', '照片5', '照片6', '照片(推薦頁)']
    for i, row in enumerate(data.values):

        data_index = data.loc[i]
        data_dict= data_index.to_dict()
        data_dict['name'] = data_dict.pop('店名')
        data_dict['address'] = data_dict.pop('地址(A-格式不限)')
        data_dict['lat'] = data_dict.pop('緯度')
        data_dict['lon'] = data_dict.pop('經度')
        data_dict['tel'] = data_dict.pop('電話')
        data_dict['bussiness_time'] = data_dict.pop('開放時間(統一格式)')
        data_dict['updtime'] = data_dict.pop('近期更新時間')
        data_dict['updtime'] = str(data_dict['updtime'])[:6]

        img_list = []
        data_dict['imgs'] = img_list
        for key, value in data_dict.items():
            if key in img_ch_list:
                if value != "":
                    img_list.append(value)

        del data_dict['照片0__(fb目前頭貼)'], data_dict['照片1'], data_dict['照片2'], data_dict['照片3'], data_dict['照片4'], data_dict['照片5'], data_dict['照片6'], data_dict['照片(推薦頁)']
        green_restaurant.append(data_dict)
        if data_dict['lon'] == "" or data_dict['lat'] == "":
            del green_restaurant[i]

    return green_restaurant


def get_reed_datas():
    df = pd.read_excel(os.path.join(settings.DATA_ROOT, "plants.xlsx"))
    fetched_reed_datas = df.loc[df['vernacularName'].isin(['臺灣蘆竹', '蘆竹', '蘆葦', '臺灣蘆葦', '開卡蘆'])]
    header = ['decimalLongitude','decimalLatitude', 'vernacularName']
    filter_header_data = fetched_reed_datas[header]

    reed_list = []
    for index, row in filter_header_data.iterrows():
        data_index = filter_header_data.loc[index]
        data_dict = data_index.to_dict()
        data_dict['name'] = data_dict.pop('vernacularName')
        data_dict['lat'] = data_dict.pop('decimalLatitude')
        data_dict['lon'] = data_dict.pop('decimalLongitude')
        reed_list.append(data_dict)
        if data_dict['lon'] == "" or data_dict['lat'] == "":
            del reed_list[index]

    return reed_list


def get_solitary_bee_hotel():
    file_name = 'solitary_bee_hotel.geojson'
    file_datas = {}
    with open(os.path.join(settings.DATA_ROOT, file_name)) as f:
        file_datas = json.loads(f.read())

    return file_datas["features"]
