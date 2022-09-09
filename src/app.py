from __future__ import annotations

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'message': 'Hello World!'}
