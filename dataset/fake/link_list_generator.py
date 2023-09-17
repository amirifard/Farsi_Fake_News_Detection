files = ['allfacts_1.txt', 'allfacts_2.txt', 'allfacts_3.txt', 'allfacts_4.txt', 'allfacts_5.txt']

import ast, json

all_dicts = []
# Read the string representation of the dictionary from the text file
for f in files:
    with open(f, 'r') as file:
        dict_str = file.read()

    # Convert the string back to a dictionary
    data = ast.literal_eval(dict_str)
    all_dicts.append(data)

base_url = 'https://factnameh.com/fa/fact-checks/'

all_articles = []
for batch in all_dicts:
    for node in batch['data']['factcheckArticles']['edges']:
        if node['node']['published']:
            if node['node']['slug']:
                if node['node']['rating']:
                    article_part = node['node']['published'] +'-'+ node['node']['slug']
                    full_link = base_url + article_part
                    article_category = node['node']['rating']['titleEn']
                    all_articles.append({'type' : article_category, 'url' : full_link})


with open('all_articles.json', 'w') as file:
    json.dump(all_articles, file)