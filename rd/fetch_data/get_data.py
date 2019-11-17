import pandas as pd
import numpy as np
import os
import json
import sys
import csv


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
        data_dict['id'] = i+1
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

    with open(os.path.join(settings.DATA_ROOT, 'green_restaurant.json'), 'w') as f:
        json.dump(green_restaurant, f)

    # return json.dumps(green_restaurant)

# get_green_restaurant_data()

def write_to_green_restaurant_csv(green_restaurant):
    with open('green_restaurant.csv', 'w', newline='') as csvFile:
        # 定義欄位
        fieldNames = ['id', 'name', 'address', 'lat', 'lon', 'tel', 'bussiness_time', 'updtime', 'imgs']

        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvFile, fieldNames)

        # 寫入第一列的欄位名稱
        writer.writeheader()

        # 寫入資料
        for green in green_restaurant:
            writer.writerow(green)

# input_green_restaurant = get_green_restaurant_data()

# write_to_green_restaurant_csv(input_green_restaurant)


def get_reed_and_river_data():
    df = pd.read_excel(os.path.join(settings.DATA_ROOT, "product_reed_river.xlsx"))
    header = ["id",	"catalogNumber", "recordedBy", "eventDate", "locality", "decimalLatitude",
    "decimalLongitude",	"identifiedBy",	"scientificName", "family", "vernacularName", "產地照片",
    "產地標本照片",	"空拍照片", "測站名稱", "測站編號", "經度", "緯度", "河川汙染指數", "測站圖片URL", "測站RUL"]

    filter_reed_datas = df.loc[df['vernacularName'].isin(['臺灣蘆竹', '蘆竹', '蘆葦', '臺灣蘆葦', '開卡蘆'])]
    fetched_reed_datas = filter_reed_datas[header]

    data = fetched_reed_datas.replace(np.nan, '', regex=True)
    img_data_reed_list = ["產地照片", "產地標本照片", "空拍照片"]
    img_data_river_list = ["測站圖片URL", "測站RUL"]

    reed_river_list = []
    for index, row in data.iterrows():
        data_index = data.loc[index]
        data_dict = data_index.to_dict()
        data_dict['id'] = data_dict.pop('id')
        data_dict['name'] = data_dict.pop('vernacularName')
        data_dict['lon'] = data_dict.pop('decimalLongitude')
        data_dict['lat'] = data_dict.pop('decimalLatitude')

        river_dict= {}
        river_dict['name'] = data_dict.pop('測站名稱')
        river_dict['station_id'] = data_dict.pop('測站編號')
        river_dict['lon'] = data_dict.pop('經度')
        river_dict['lat'] = data_dict.pop('緯度')
        river_dict['pollution_index'] = data_dict.pop('河川汙染指數')

        data_dict['river'] = river_dict

        img_reed_list = []
        img_river_list = []
        data_dict['imgs'] = img_reed_list
        river_dict['imgs'] = img_river_list
        for key, value in data_dict.items():
            if key in img_data_reed_list:
                if value != "":
                    if key == "空拍照片" or key == '測站圖片URL':
                        img = os.path.join(settings.DATA_URL, 'reed_shot', value)
                    else:
                        img = value
                    img_reed_list.append(img)

            if key in img_data_river_list:
                if value != "":
                    if key == "空拍照片" or key == '測站圖片URL':
                        img = os.path.join(settings.DATA_URL, 'reed_shot', value)
                    else:
                        img = value
                    img_river_list.append(img)

        del data_dict['產地照片'], data_dict['產地標本照片'], data_dict['空拍照片'], data_dict["測站圖片URL"], data_dict["測站RUL"], data_dict['catalogNumber'], data_dict['eventDate']

        if (data_dict['river']['lon'] == '' or data_dict['river']['lon'] == ''):
            continue
        reed_river_list.append(data_dict)

    with open(os.path.join(settings.DATA_ROOT, 'reed_river_all.json'), 'w') as f:
        json.dump(reed_river_list, f)

# get_reed_and_river_data()

# def get_reed_datas():
#     df = pd.read_excel(os.path.join(settings.DATA_ROOT, "plants.xlsx"))
#     fetched_reed_datas = df.loc[df['vernacularName'].isin(['臺灣蘆竹', '蘆竹', '蘆葦', '臺灣蘆葦', '開卡蘆'])]
#     header = ['id', 'decimalLongitude','decimalLatitude', 'vernacularName']
#     filter_header_data = fetched_reed_datas[header]

#     reed_list = []
#     for index, row in filter_header_data.iterrows():
#         data_index = filter_header_data.loc[index]
#         data_dict = data_index.to_dict()
#         data_dict['name'] = data_dict.pop('vernacularName')
#         data_dict['lat'] = data_dict.pop('decimalLatitude')
#         data_dict['lon'] = data_dict.pop('decimalLongitude')
#         if (data_dict['lon'] == 120.0502778 or data_dict['lat'] == 24.75027778) or (data_dict['lon'] == "" or data_dict['lat'] == ""):
#             continue

#         data_dict['img'] = get_reed_shot_img(data_dict['id'])
#         reed_list.append(data_dict)

#     with open(os.path.join(settings.DATA_ROOT, 'reed_data.json'), 'w') as f:
#         json.dump(reed_list, f)
#     # return json.dumps(reed_list)

def get_reed_shot_img(reed_id):
    img = ''
    folder = os.path.join(settings.DATA_ROOT, 'reed_shot')
    if os.path.isdir(folder):
        file_name = reed_id + '.jpg'
        if os.path.isfile(os.path.join(folder, file_name)):
            img = os.path.join(settings.DATA_URL, 'reed_shot', file_name)

    return img


def write_to_reed_csv(reed_list):
    with open('reed_data.csv', 'w', newline='') as csvFile:
        # 定義欄位
        fieldNames = ['name', 'lat', 'lon']

        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvFile, fieldNames)

        # 寫入第一列的欄位名稱
        writer.writeheader()

        # 寫入資料
        for rd in reed_list:
            writer.writerow(rd)

# reed_list = get_reed_datas()

# write_to_reed_csv(reed_list)

def get_solitary_bee_hotel():
    file_name = 'solitary_bee_hotel.geojson'
    file_datas = {}
    with open(os.path.join(settings.DATA_ROOT, file_name)) as f:
        file_datas = json.loads(f.read())

    datas = []
    for data in file_datas["features"]:
        _data = {
            'lat': data["geometry"]["coordinates"][1],
            'lon': data["geometry"]["coordinates"][0],
            'name': data["properties"]["organization_school"],
            'id': data["properties"]["cartodb_id"]
        }
        datas.append(_data)

    return datas


def get_water_quality_data():
    df = pd.read_excel(os.path.join(settings.DATA_ROOT, "water_quality.xlsx"))
    data = df.replace(np.nan, '', regex=True)
    water_qc_data = []

    for index, row in data.iterrows():
        data_index = data.loc[index]
        data_dict = data_index.to_dict()
        data_dict['river'] = data_dict.pop('河流')
        data_dict['station'] = data_dict.pop('測站名稱')
        data_dict['river_pollution_index'] = data_dict.pop('河川污染指數')
        data_dict['lon'] = data_dict.pop('經度')
        data_dict['lat'] = data_dict.pop('緯度')
        data_dict['station_img'] = data_dict.pop('測站照片')
        data_dict['station_url'] = data_dict.pop('測站網址')

        water_qc_data.append(data_dict)
        if data_dict['river'] == '':
            data_dict.update({
                'river': water_qc_data[index-1]['river']
            })

    reconstruct_water_quality = []
    for water in water_qc_data:
        if water['lon'] == "" or water['lat'] == "":
            continue
        reconstruct_water_quality.append(water)

    return reconstruct_water_quality

# get_water_quality_data()