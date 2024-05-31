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
table_name = "edu_bigdata_user_video"
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
    class INTEGER NOT NULL,
    month INTEGER NOT NULL,
    indicator VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    video_item_sn INTEGER NOT NULL,
    review_sn INTEGER NOT NULL,
    review_start_timestamp INTEGER NOT NULL,
    review_end_timestamp INTEGER NOT NULL,
    review_start_time TIMESTAMP NOT NULL,
    review_end_time TIMESTAMP NOT NULL,
    review_total_time INTEGER NOT NULL,
    review_finish_rate INTEGER NOT NULL
);
'''
cur.execute(sql_command)
conn.commit()

# read data form csv to database
selected_columns = [
    "PseudoID",
    "city_code",
    "organization_id",
    "grade",
    "class",
    "month",
    "indicator",
    "subject",
    "video_item_sn",
    "review_sn",
    "review_start_timestamp",
    "review_end_timestamp",
    "review_start_time",
    "review_end_time",
    "review_total_time",
    "review_finish_rate",
]

data = pandas.read_csv('data/edu_bigdata_2024.csv', usecols=selected_columns)

for index, row in data.iterrows():
    pseudo_id = str_to_int(row['PseudoID'])
    city_code = row['city_code']
    organization_id = str_to_int(row['organization_id'])
    grade = str_to_int(row['grade'])
    user_class = str_to_int(row['class'])
    month = str_to_int(row['month'])
    indicator = row['indicator']
    subject = row['subject']
    video_item_sn = str_to_int(row['video_item_sn'])
    review_sn = str_to_int(row['review_sn'])
    review_start_timestamp = str_to_int(row['review_start_timestamp'])
    review_end_timestamp = str_to_int(row['review_end_timestamp'])
    review_start_time = row['review_start_time']
    review_end_time = row['review_end_time']
    review_total_time = str_to_int(row['review_total_time'])
    review_finish_rate = str_to_int(row['review_finish_rate'])

    sql_command = f'''
    INSERT INTO {table_name} 
        (pseudo_id, city_code, organization_id, grade, class, month, indicator, subject, video_item_sn, review_sn, review_start_timestamp, review_end_timestamp, review_start_time, review_end_time, review_total_time, review_finish_rate)
    VALUES 
        ({pseudo_id}, '{city_code}', {organization_id}, {grade}, {user_class}, {month}, '{indicator}', '{subject}', {video_item_sn}, {review_sn}, {review_start_timestamp}, {review_end_timestamp}, '{review_start_time}', '{review_end_time}', {review_total_time}, {review_finish_rate})
    '''

    cur.execute(sql_command)

conn.commit()

# create videos tables
cur.execute(f"DROP TABLE IF EXISTS videos")
cur.execute(f"CREATE TABLE videos AS (SELECT DISTINCT video_item_sn, subject, indicator FROM {table_name})")
conn.commit()

# create user_review_video_logs tables
cur.execute(f"DROP TABLE IF EXISTS user_review_video_logs")
cur.execute(f'''
    CREATE TABLE user_review_video_logs AS
    (
        SELECT DISTINCT 
        review_sn, 
        pseudo_id, 
        video_item_sn, 
        review_start_timestamp, 
        review_end_timestamp, 
        review_start_time, 
        review_end_time, 
        review_total_time, 
        review_finish_rate
        FROM {table_name}
    );
''')
conn.commit()

# drop tamp table
cur.execute(f"DROP TABLE IF EXISTS {table_name}")
conn.commit()

cur.close()
conn.close()

print("crate videos, user_review_video_logs is successfully")