import json

with open('chosen_author_books.txt', 'r') as file:
    dict_with_books = dict(json.load(file))

sorted_list_of_titles = sorted(dict_with_books, key=lambda x: sum(dict_with_books[x].values()), reverse=True)
sorted_list_of_dicts = [{x : dict_with_books[x]} for x in sorted_list_of_titles]

with open('chosen_author_books_sorted.txt', 'w') as file:
    file.write(str(sorted_list_of_titles)+'\n'+str(sorted_list_of_dicts))