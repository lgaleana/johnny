from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
import openai
import os

app = FastAPI()


class UrlInput(BaseModel):
    url: HttpUrl


@app.get('/')
def hello_world():
    return {'message': 'Hello, World!'}


@app.post('/input_url')
def input_url(url_input: UrlInput):
    url = url_input.url
    html_content = scrape_url(url)
    extracted_info = extract_info_with_chatgpt(html_content)
    return {'message': 'URL received', 'url': url, 'html_content': html_content, 'extracted_info': extracted_info}


def scrape_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return split_html_content(response.text)
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=400, detail=str(err))


def split_html_content(html_content):
    return [html_content[i:i+400000] for i in range(0, len(html_content), 400000)]


def extract_info_with_chatgpt(html_content_list):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    extracted_info = ''
    for html_content in html_content_list:
        response = openai.ChatCompletion.create(
          model='gpt-4-turbo',
          messages=[
                {'role': 'system', 'content': 'You are a helpful assistant. Extract the name of the reviewer, the review, the rating, the date, and an image (if available) from the following HTML content.'},
                {'role': 'user', 'content': html_content}
            ]
        )
        extracted_info += response['choices'][0]['message']['content'] + '\n-----\n'
    return extracted_info
