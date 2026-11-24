"""Повышенная сложность, задание 4: загрузка файла через форму."""
from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template_string, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

PAGE = """<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>Загрузка файла</title></head>
<body>
  <h1>Загрузка файла</h1>
  <p>Разрешены TXT, PDF, PNG, JPG и JPEG, размер до 5 МБ.</p>
  <form method="post" enctype="multipart/form-data">
    <label for="file">Файл:</label>
    <input id="file" name="file" type="file" accept=".txt,.pdf,.png,.jpg,.jpeg" required>
    <button type="submit">Загрузить</button>
  </form>
  {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>"""


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template_string(PAGE, message="")
    file = request.files.get("file")
    if not file or not file.filename:
        return render_template_string(PAGE, message="Выберите файл."), 400
    # Имя не используется как путь: сервер создаёт случайное имя файла.
    original_name = secure_filename(file.filename)
    extension = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""
    if extension not in ALLOWED_EXTENSIONS:
        return render_template_string(PAGE, message="Недопустимый тип файла."), 400
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid4().hex}.{extension}"
    file.save(UPLOAD_DIR / stored_name)
    return render_template_string(PAGE, message=f"Файл сохранён: {stored_name}")


@app.errorhandler(413)
def too_large(error):
    return render_template_string(PAGE, message="Файл слишком большой: максимум 5 МБ."), 413


if __name__ == "__main__":
    app.run()
