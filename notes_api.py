"""Повышенная сложность, задание 10: API для проверки с pytest."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="API заметок для тестирования")
notes: dict[int, str] = {}
next_id = 1


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>Заметки</title></head>
<body>
  <h1>Заметки</h1>
  <form id="create-form">
    <label for="text">Текст заметки:</label>
    <input id="text" maxlength="200" required>
    <button type="submit">Создать</button>
  </form>
  <p>Для получения или удаления введите номер заметки:</p>
  <label for="note-id">Номер:</label>
  <input id="note-id" type="number" min="1">
  <button type="button" id="get">Получить</button>
  <button type="button" id="delete">Удалить</button>
  <p id="result" aria-live="polite"></p>
  <script>
    const result = document.getElementById('result');
    const noteId = document.getElementById('note-id');
    document.getElementById('create-form').addEventListener('submit', async (event) => {
      event.preventDefault();
      try {
        const response = await fetch('/notes', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({text: document.getElementById('text').value})
        });
        if (!response.ok) { result.textContent = 'Не удалось создать заметку.'; return; }
        const note = await response.json();
        noteId.value = note.id;
        result.textContent = `Создана заметка №${note.id}: ${note.text}`;
      } catch (error) { result.textContent = 'Ошибка соединения с сервером.'; }
    });
    async function handleNote(method) {
      if (!noteId.value || !noteId.checkValidity()) {
        result.textContent = 'Введите положительный номер заметки.';
        return;
      }
      try {
        const response = await fetch('/notes/' + encodeURIComponent(noteId.value), {method});
        if (response.status === 404) { result.textContent = 'Заметка не найдена.'; return; }
        if (!response.ok) { result.textContent = 'Ошибка запроса.'; return; }
        if (method === 'DELETE') { result.textContent = 'Заметка удалена.'; return; }
        const note = await response.json();
        result.textContent = `Заметка №${note.id}: ${note.text}`;
      } catch (error) { result.textContent = 'Ошибка соединения с сервером.'; }
    }
    document.getElementById('get').addEventListener('click', () => handleNote('GET'));
    document.getElementById('delete').addEventListener('click', () => handleNote('DELETE'));
  </script>
</body>
</html>"""


class NoteInput(BaseModel):
    text: str = Field(min_length=1, max_length=200)


@app.post("/notes", status_code=201)
def create_note(note: NoteInput):
    global next_id
    note_id = next_id
    next_id += 1
    notes[note_id] = note.text
    return {"id": note_id, "text": note.text}


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return {"id": note_id, "text": notes[note_id]}


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    del notes[note_id]
