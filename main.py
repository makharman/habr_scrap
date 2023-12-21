import requests
from bs4 import BeautifulSoup
import json

data = []

for i in range(1,3):
    print(f'Parsing {i} page')
    url = f'https://career.habr.com/vacancies?page={i}&skills[]=1012&type=all' 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all("div",class_='vacancy-card__inner')

    for card in cards:
        card_url = card.a['href']
        url = f'https://career.habr.com{card_url}' 
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text,'lxml')
        company = soup.find("div", 'company_name')
        print(company.text)   
        job_title = soup.find("h1", 'page-title__title')
        print(job_title.text)      
        skills = soup.find("span", 'inline-list')
        print(skills.text) 

        vacancy_data = {
            'company': company.text.strip(),
            'job_title': job_title.text.strip(),
            'skills': skills.text.strip() 
        }

        data.append(vacancy_data)

with open('./vacancies.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp, indent=2, ensure_ascii=False)
