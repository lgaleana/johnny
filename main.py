from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
import openai

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
        return response.text
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=400, detail=str(err))


def extract_info_with_chatgpt(html_content):
    openai.api_key = 'your-api-key'
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": html_content}
        ]
    )
    return response['choices'][0]['message']['content']
