import requests
import sqlite3

def create_table():
    conn = sqlite3.connect('hacker_news.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stories(id INTEGER PRIMARY KEY,
               title TEXT, user TEXT, score INTEGER, time INTEGER, url TEXT)''')
    conn.commit()
    conn.close()

def insert_story(story):
    conn = sqlite3.connect('hacker_news.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO stories(title, user, score, url) VALUES (?, ?, ?, ?, ?)",
              (story["Title"], story["User"], story["Score"], story["Time"], story["URL"]))
    conn.commit()
    conn.close()

def get_last_100():
    url = "https://hacker-news.firebaseio.com/v0/topstories"
    response = requests.get(url)
    
    top_stories_ids = response.json()[:100]

    table_data = []
    for story_id in top_stories_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = requests.get(story_url)
        story_data = story_response.json()

        # Extract relevant information
        title = story_data.get("title")
        user = story_data.get("user")
        score = story_data.get("score")
        time = story_data.get("time")
        url = story_data.get("url")

        table_data.append({"Title":title, "User":user, "Score":score, "Time":time, "Url":url})

    return table_data

create_table()
table = get_last_100()
for row in table:
    insert_story(row)