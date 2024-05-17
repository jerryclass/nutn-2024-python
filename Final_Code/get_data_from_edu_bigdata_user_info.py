import pandas
import psycopg2


# string convert int
def str_to_int(str):
    try:
        num = int(str)
    except ValueError:
        num = int(0)
    return num


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
table_name = "edu_bigdata_user_info"
sql_command = f"DROP TABLE IF EXISTS {table_name}"
cur.execute(sql_command)
conn.commit()

sql_command = f'''
CREATE TABLE {table_name} (
    id SERIAL PRIMARY KEY,
    pseudo_id INTEGER NOT NULL,
    city_code VARCHAR(100) NOT NULL,
    organization_id INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    class INTEGER NOT NULL
);
'''
cur.execute(sql_command)
conn.commit()

# read data form csv to database
selected_columns = ["PseudoID", "city_code", "organization_id", "grade", "class"]

data = pandas.read_csv('data/edu_bigdata_2024.csv', usecols=selected_columns)

for index, row in data.iterrows():
    pseudo_id = str_to_int(row['PseudoID'])
    city_code = row['city_code']
    organization_id = str_to_int(row['organization_id'])
    grade = str_to_int(row['grade'])
    user_class = str_to_int(row['class'])

    sql_command = f"INSERT INTO {table_name} (pseudo_id, city_code, organization_id, grade, class) VALUES ({pseudo_id}, '{city_code}', {organization_id}, {grade}, {user_class})"
    cur.execute(sql_command)

conn.commit()
cur.close()
conn.close()

print("資料產生完成")