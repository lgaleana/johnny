from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests

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
    return {'message': 'URL received', 'url': url, 'html_content': html_content}


def scrape_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=400, detail=str(err))
