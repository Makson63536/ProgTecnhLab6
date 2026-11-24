"""Средняя сложность, задание 8: FastAPI принимает параметр."""
from fastapi import FastAPI, Query

app = FastAPI(title="Приветствие по параметру")


@app.get("/")
def instructions():
    return {"message": "Чтобы ввести имя, добавьте к адресу /hello?name=ВашеИмя"}


@app.get("/hello")
def hello(name: str = Query(..., min_length=1, max_length=100)):
    return {"message": f"Привет, {name}!"}
