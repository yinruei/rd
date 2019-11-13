import pandas as pd

def get_green_restaurant_data():
    green_restaurant = []
    df = pd.read_excel("data.xlsx", sheet_name="A綠餐廳蔬食")
    header = ['店名', '地址(A-格式不限)', '經度', '緯度', '電話', '開放時間(統一格式)',
            '照片0__(fb目前頭貼)', '照片1','照片2', '照片3', '照片4', '照片5', '照片6',
            '照片(推薦頁)','近期更新時間']

    data = df[header]
    context = {}
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

        img_list = []
        data_dict['imgs'] = img_list

        for key, value in data_dict.items():
            if key in img_ch_list:
                if value is not None:
                    img_list.append(value)

        del data_dict['照片0__(fb目前頭貼)'], data_dict['照片1'], data_dict['照片2'], data_dict['照片3'], data_dict['照片4'], data_dict['照片5'], data_dict['照片6'], data_dict['照片(推薦頁)']
        green_restaurant.append(data_dict)

    return green_restaurant

get_green_restaurant_data()
