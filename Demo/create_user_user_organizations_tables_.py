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

# init temp table
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

# create user_data_table
for index, row in data.iterrows():
    pseudo_id = str_to_int(row['PseudoID'])
    city_code = row['city_code']
    organization_id = str_to_int(row['organization_id'])
    grade = str_to_int(row['grade'])
    user_class = str_to_int(row['class'])

    sql_command = f"INSERT INTO {table_name} (pseudo_id, city_code, organization_id, grade, class) VALUES ({pseudo_id}, '{city_code}', {organization_id}, {grade}, {user_class})"
    cur.execute(sql_command)

conn.commit()

# create users tables
cur.execute(f"DROP TABLE IF EXISTS users")
cur.execute(f"CREATE TABLE users AS (SELECT DISTINCT pseudo_id, city_code FROM {table_name})")
conn.commit()

# create user_organizations tables
cur.execute(f"DROP TABLE IF EXISTS user_organizations")
cur.execute(f"CREATE TABLE user_organizations AS (SELECT DISTINCT pseudo_id, organization_id, grade, class FROM {table_name})")
conn.commit()

# drop tamp table
cur.execute(f"DROP TABLE IF EXISTS {table_name}")
conn.commit()

cur.close()
conn.close()

print("crate user, user_organizations is successfully")