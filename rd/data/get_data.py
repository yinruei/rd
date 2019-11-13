import pandas as pd
import xlrd
import openpyxl

def get_green_restaurant_data():
    green_restaurant = []
    df = pd.read_excel("data.xlsx", sheet_name="A綠餐廳蔬食")
    print(type(df))
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

        # del data_dict['照片0__(fb目前頭貼)']
        green_restaurant.append(data_dict)
    # print(green_restaurant)

    # data = df[
    #             ['店名', '地址(A-格式不限)', '經度', '緯度', '電話',
    #             '開放時間(統一格式)', '照片0__(fb目前頭貼)', '照片1',
    #             '照片2', '照片3', '照片4', '照片5', '照片6', '照片(推薦頁)',
    #             '近期更新時間'
    #             ]
    #         ]
    # print(data)
    # print(type(data))
    # print(data.keys())
    # print({col:data[col].tolist() for col in data.columns})
    # print('222', data)
    # print('122', a)
    # b = a.to_dict()
    # print(b)
    # d = data.to_dict()
    # for key, value in d.items():
    #     print('key', key)
    #     print('------------')
    #     for k in value:
    #         print(value[k])
    # print(d)

    # green_restaurant.append(data)

get_green_restaurant_data()

# def get_data():
#     context = {}
#     workbook =openpyxl.load_workbook('data.xlsx')
#     # print(workbook.sheet_names())                  #查看所有sheet
#     booksheet = workbook.sheet_by_name('A綠餐廳蔬食')  #或用名称取sheet
#     print(booksheet
#
# .name)
#     row3=[item.value for item in list(booksheet.rows)[2]]
#     print(row2)
#     # a = booksheet.row_values(0, 6, 10)
#     # rows = booksheet.nrows #(列)
#     # col = booksheet.ncols #欄位(行)
#     # for i in range(1, 3):
#     #     print('---', booksheet.row_values(i))
#     # #读单元格数据
#     # cell_11 = booksheet.cell_value(0,1)
#     # cell_21 = booksheet.cell_value(1,0)
#     #读一行数据
#     # for i in range(1,3):
#     #     row_3 = booksheet.row_values(i)
#     #     print(row_3)
#     # row_3 = booksheet.row_values(3)
#     # print(cell_11)

# get_data()