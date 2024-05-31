import pandas
import psycopg2
from psycopg2.extras import DictCursor
import matplotlib.pyplot as plt

# connect to postgres database
conn = psycopg2.connect(
    dbname="nutn",
    user="nutn",
    password="nutn@password",
    host="172.18.8.152",
    port="5432",
)
cur = conn.cursor()

cur.execute('''
    SELECT videos.subject , ROUND(AVG(user_review_video_logs.review_total_time),2) as avg_time
    FROM user_review_video_logs
    LEFT JOIN videos ON user_review_video_logs.video_item_sn = videos.video_item_sn
    GROUP BY videos.subject
    ORDER BY avg_time DESC
''')
results = cur.fetchall()

print("查詢每個影片類別的平均觀看時間")
for row in results:
    subject = row[0]
    avg_time = row[1]
    print(f"影片類別: {subject}, 平均觀看時間: {avg_time} 秒")

# fetch data
subjects = [row[0] for row in results]
avg_times = [row[1] for row in results]

# use Matplotlib 
plt.figure(figsize=(10, 6))
plt.bar(subjects, avg_times, color='skyblue')
plt.xlabel('影片類別')
plt.ylabel('平均觀看時間 (秒)')
plt.title('影片類別與平均觀看時間')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('average_view_time.png')

