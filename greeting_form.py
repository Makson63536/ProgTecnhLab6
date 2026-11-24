"""Средняя сложность, задание 2: форма с именем и приветствием."""
from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>Приветствие</title></head>
<body>
  <h1>Введите имя</h1>
  <form method="post">
    <label for="name">Имя:</label>
    <input id="name" name="name" maxlength="100" required>
    <button type="submit">Отправить</button>
  </form>
  {% if name %}<p>Привет, {{ name }}!</p>{% endif %}
  {% if error %}<p>{{ error }}</p>{% endif %}
</body>
</html>"""


@app.route("/", methods=["GET", "POST"])
def greeting():
    name = ""
    error = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            error = "Введите имя."
        elif len(name) > 100:
            name = ""
            error = "Имя должно содержать не более 100 символов."
    return render_template_string(PAGE, name=name, error=error)


if __name__ == "__main__":
    app.run()
