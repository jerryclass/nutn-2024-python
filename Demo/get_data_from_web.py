import requests
import json
import psycopg2


# string convert int
def str_to_int(str):
    try:
        num = int(str)
    except ValueError:
        num = int(0)
    return num


# opendata url
url = 'https://opendataap2.e-land.gov.tw/./resource/files/2021-08-27/6961cfab1067bd0f6faae77af04cda09.json'

# get edu_level data from restful api
response = requests.get(url, verify=False)

if response.status_code == 200:
    json_objects = response.json()
else:
    print('Failed to fetch data:', response.status_code)

json_string = json.dumps(json_objects).replace(" ", "")
json_objects = json.loads(json_string)


# connect to postgres database
conn = psycopg2.connect(
    dbname="nutn",
    user="nutn",
    password="nutn@password",
    host="172.18.8.152",
    port="5432",
)
cur = conn.cursor()

# init table
table_name = "edu_level"
sql_command = f"DROP TABLE IF EXISTS {table_name}"
cur.execute(sql_command)
conn.commit()

sql_command = '''
CREATE TABLE edu_level (
    "id" SERIAL PRIMARY KEY,
    "year" INTEGER NOT NULL,
    "area" VARCHAR(100) NOT NULL,
    "gender" VARCHAR(100) NOT NULL,
    "literacy" INTEGER NOT NULL,
    "phd_completion" INTEGER NOT NULL,
    "phd_non_completion" INTEGER NOT NULL,
    "ms_completion" INTEGER NOT NULL,
    "ms_non_completion" INTEGER NOT NULL,
    "bs_completion" INTEGER NOT NULL,
    "bs_non_completion" INTEGER NOT NULL
);
'''
cur.execute(sql_command)
conn.commit()


for json_object in json_objects:
    year = str_to_int(json_object['年度'])
    area = json_object['區域']
    gender = json_object['性別']
    literacy = str_to_int(json_object['識字者合計'])
    phd_completion = str_to_int(json_object['博士畢業'])
    phd_non_completion = str_to_int(json_object['博士肄業'])
    ms_completion = str_to_int(json_object['研究所畢業'])
    ms_non_completion = str_to_int(json_object['研究所肄業'])
    bs_completion = str_to_int(json_object['大學(含獨立學院)畢業'])
    bs_non_completion = str_to_int(json_object['大學(含獨立學院)肄業'])

    if year != "" and gender != "計":
        sql_command = f"INSERT INTO {table_name} (year, area, gender, literacy, phd_completion, phd_non_completion, ms_completion, ms_non_completion, bs_completion, bs_non_completion) VALUES ('{year}', '{area}', '{gender}', {literacy}, {phd_completion}, {phd_non_completion}, {ms_completion}, {ms_non_completion}, {bs_completion}, {bs_non_completion})"
        cur.execute(sql_command)

conn.commit()
cur.close()
conn.close()

print("資料產生完成")
