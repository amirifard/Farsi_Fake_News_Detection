from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os
from datetime import datetime
import aiohttp
import asyncio
import time
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

START = 1               # Initial news article code
END = 1_186_547         # Final news article code
CONC = 100              # Concurrent requests
SAVE_INTERVAL = 10_000  # Save intervals to disk

async def extract_elements(session, url):
    # Send a GET request to the URL
    try:
        async with session.get(url) as response:
        
            # If the GET request is successful, the status code will be 200
            if response.status == 200:
                
                # Get the content of the response
                page_content = await response.text()
                
                # Create a BeautifulSoup object and specify the parser
                soup = BeautifulSoup(page_content, 'html.parser')
                
                # Find h1 elements by class name
                elements_class_Htag = soup.find_all('h1', class_='Htag')
                
                # Find div elements by class name and id
                elements_class_body_id_newsMainBody = soup.find('div', attrs={"class": "body", "id": "newsMainBody"})

                # Find div with class "news_path"
                news_path = soup.find('div', class_='news_path')
                page, category = '', ''
                if news_path:
                    links = news_path.find_all('a')
                    if links:
                        page = links[0].text.strip() if len(links) > 0 else ''
                        category = links[1].text.strip() if len(links) > 1 else ''

                # Find span with class "en_date visible-lg visible-md"
                date_span = soup.find('span', class_='en_date visible-lg visible-md')
                date = ''
                if date_span:
                    date_text = date_span.text.strip()
                    date_obj = datetime.strptime(date_text, '%d %B %Y')
                    date = date_obj.strftime('%Y-%m-%d')

                # Find div with class "tag_items"
                tag_items = soup.find('div', class_='tag_items')
                tags = []
                if tag_items:
                    a_tags = tag_items.find_all('a')
                    tags = [a_tag.text.strip() for a_tag in a_tags]

                title = ''.join([element.text.strip() for element in elements_class_Htag])
                content = ''.join([element.text.strip() for element in elements_class_body_id_newsMainBody.find_all('p')]) if elements_class_body_id_newsMainBody else ''
                res = {
                    'url': url,
                    'title': ILLEGAL_CHARACTERS_RE.sub(r'',title),
                    'content': ILLEGAL_CHARACTERS_RE.sub(r'',content),
                    'page': ILLEGAL_CHARACTERS_RE.sub(r'',page),
                    'category': ILLEGAL_CHARACTERS_RE.sub(r'',category),
                    'date': date,
                    'tags': tags
                }
                # if len(title) > 0:
                #     print("\r" + " " * 100 + f'\rNews: {title}', end='', flush=True)
                return res

            else:
                #print(await response.text())
                #print(f'skipped : {url}')
                pass
    except Exception as e:
        print(f"\rAn error occurred while processing the URL {url}: {e}")

# DataFrame columns
df = pd.DataFrame(columns=['url', 'title', 'content', 'page', 'category', 'date', 'tags'])

async def main(urls, df):
    async with aiohttp.ClientSession() as session:
        # print('')
        tasks = [extract_elements(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for result in results:
            df = df.append(result, ignore_index=True)
        # os.system('clear')
    
    return df

for i in tqdm(range(START, END, CONC)):
    
    urls = [f'https://www.tabnak.ir/fa/news/{n}/' for n in range(i,i+CONC)]
    df = asyncio.run(main(urls, df))
        
    # Save the dataframe every 10000 iterations
    if i % SAVE_INTERVAL == 0 and i != START:
        df.to_excel(f'tabnak_{i-SAVE_INTERVAL}_to_{i}.xlsx', index=False)
        df = pd.DataFrame(columns=['url', 'title', 'content', 'page', 'category', 'date', 'tags'])  # Clear the dataframe
        time.sleep(10)

# save the dataframe for the last chunk
df.to_excel(f'tabnak_{END-SAVE_INTERVAL}_to_{END}.xlsx', index=False)