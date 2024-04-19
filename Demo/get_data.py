import requests
import json


def str_to_int(str):
    try:
        num = int(str)
    except ValueError:
        num = int(0)
    return num

url = 'https://opendataap2.e-land.gov.tw/./resource/files/2021-08-27/6961cfab1067bd0f6faae77af04cda09.json'

response = requests.get(url, verify=False)

if response.status_code == 200:
    json_objects = response.json()
else:
    print('Failed to fetch data:', response.status_code)

json_string = json.dumps(json_objects).replace(" ", "")
json_objects = json.loads(json_string)
# ------------------------------------------------------


file_path = 'example.txt'
with open(file_path, 'w') as file:
    for json_object in json_objects:
        if json_object['性別'] == '計':
            year = json_object['年度']
            area = json_object['區域']
            total_num = str_to_int(json_object['總計'])
            phd_num = str_to_int(json_object['博士畢業'])
            ms_num = str_to_int(json_object['研究所畢業'])

            high_grade_num = ms_num + phd_num
            high_rate = high_grade_num/total_num

            file.write(f"年度:{year} 區域:{area} 總人口數:{total_num} 研究所以上學歷人數:{high_grade_num} 所占比例:{high_rate:.4%} \n")

print("資料產生完成")


