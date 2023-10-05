import json
import requests
import pandas as pd
import time

#Дата, с которой происходит первый запрос
date = ''

#Если дата - пустая строка, то сайт выдаёт информацию по последней, ещё не законченной, неделе.
#В этой информации будет указана дата прошлого недельного списка, которую мы берём для нового запроса. 
#И так далее, по одной неделе двигаемся назад

#Имя автора, книги которого будем искать
name_of_author = 'Dan Brown'

#Создаём файлы или очищаем уже созданные файлы
with open('all_books_overall.txt', 'w') as file:
    file.write("[]")
with open('chosen_author_books.txt', 'w') as file:
    file.write("{}")
with open('logs_every_week.txt', 'w') as file:
    pass

amount_of_weeks = 4*12*20
for _ in range(amount_of_weeks):
    text = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/full-overview.json?api-key=2W9ms29bVxmRExhq9gfcAf6ZRrgRj8Af&published_date={date}').text
    data = pd.DataFrame(json.loads(text))
    lists = pd.DataFrame(data.results.lists)
    list_of_booklists_by_genre = lists["books"]
    list_of_genre_titles = lists["list_name"]
    
    #Считываем из файла названия встреченных книг за прошлые недели
    with open('all_books_overall.txt', 'r') as file:
        saved_data = set(json.loads(file.read()))

    #Сюда запишем названия книг за текущую неделю
    set_of_current_week_books = set()

    for genre_title, list_of_book_dicts in zip(list_of_genre_titles, list_of_booklists_by_genre):
        for book_dict in list_of_book_dicts:
            set_of_current_week_books.add(book_dict['title'])
            if book_dict['author'] == name_of_author:

                #Считываем из файла dict встреченных книг выбранного автора, формат {"Название книги" : {"Название жанра топа" : кол-во недель в топе}}
                with open('chosen_author_books.txt', 'r') as file:
                    books = dict(json.loads(file.read()))

                #Если встречаем новую книгу выбранного автора или встречаю старую его книгу в новом жанре бестселлеров - обновляем информацию
                if book_dict['title'] not in books:
                    books[book_dict['title']] = {genre_title : book_dict['weeks_on_list']+1}
                elif genre_title not in books[book_dict['title']]:
                    books[book_dict['title']][genre_title] = book_dict['weeks_on_list']
                with open('chosen_author_books.txt', 'w') as file:
                    file.write(json.dumps(books))

    #Добавляем строку с информацией по новой неделе в файл с логами
    with open('logs_every_week.txt', 'a') as file:
        file.write(date+'\t'+str(json.dumps(list(set_of_current_week_books)))+'\n')

    #Пересекаем данные за текущую неделю с данными за прошлые недели 
    saved_data |= set_of_current_week_books

    #Записываем обновлённый set со списком всех книг в файл
    with open('all_books_overall.txt', 'w') as file:
        file.write(json.dumps(list(saved_data)))

    #Сохраняем дату следующей недели
    date = data['results']['previous_published_date']
    time.sleep(12)

