from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class UrlInput(BaseModel):
    url: HttpUrl


@app.get('/')
def hello_world():
    return {'message': 'Hello, World!'}


@app.post('/input_url')
def input_url(url_input: UrlInput):
    url = url_input.url
    # TODO: Pass the URL to the validation function
    return {'message': 'URL received', 'url': url}
