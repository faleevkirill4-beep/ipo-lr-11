import json
from bs4 import BeautifulSoup
import requests

url = "https://news.ycombinator.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
data = []
# Самый простой вариант
count = 1
for title in soup.find_all('span', class_='titleline'):
    data.append({
        'id':count,
        'title':title.find('a').text,
        'comments':0 })
    count += 1

comment_mas = []
count1 = 1
for comments in soup.find_all('span', class_='subline'):
    for com in comments.find_all('a'):
            if 'comment' in com.text:
                str = com.text
                num = int(str.split()[0])
                comment_mas.append({
                    'id': count1,
                    'comments': num
                })
                count1 += 1
            elif 'discuss' in com.text:
                 comment_mas.append({
                    'id': count1,
                    'comments': 0
                })
                 count1 += 1
            

for com_value in comment_mas:
        for data_value in data:
            if com_value['id'] == data_value['id']:
                 data_value['comments'] = com_value['comments']

for value in data:
    print(f"{value['id']}. Название: {value['title']} |     Комменты: {value['comments']} \n")
            

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)  

print("data.json сохранен")

html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>vibecode</title>
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
</head>
<body bgcolor="#f8f9fa">
    <h1>Таблица новостей:</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Comments</th>
        </tr>
"""

#добавляем строки в таблицу
for item in data:
    html += f"""
        <tr>
            <td>{item['id']}</td>
            <td>{item['title']}</td>
            <td>{item['comments']}</td>
        </tr>
"""

html += """
    </table>
    <a href="https://news.ycombinator.com/">Оригальный источник</a>
</body>
</html>
"""

with open ('index.html',  'w', encoding='utf-8') as file_html:
    file_html.write(html)