"""Средняя сложность, задание 6: FastAPI «Hello»."""
from fastapi import FastAPI

app = FastAPI(title="FastAPI Hello")


@app.get("/")
def hello():
    return {"message": "Hello, FastAPI!"}
