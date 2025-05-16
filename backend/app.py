from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from pathlib import Path

from database.engine import create_db, session_maker
from database.orm_query import orm_add_user, orm_get_users
from icecream import ic

# Функция для обработки событий жизненного цикла приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске приложения
    await create_db()
    yield
    # Код, выполняемый при остановке приложения (если нужно)

app = FastAPI(lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Путь к корню проекта (где лежит index.html)
PROJECT_ROOT = Path(__file__).parent.parent  # Поднимаемся на уровень выше (из backend/ в корень)
FRONTEND_DIR = PROJECT_ROOT / "frontend"    # Путь к папке frontend/

# Отдаем index.html при запросе к корню ("/")
@app.get("/")
def read_index():
    index_path = PROJECT_ROOT / "index.html"
    if not index_path.exists():
        raise RuntimeError(f"index.html не найден по пути: {index_path}")
    return FileResponse(index_path)

# Отдаем статику из frontend/src (CSS, JS)
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR / "src"),
    name="static"
)

# Отдаем HTML-страницы из frontend/pages (например, registration_successful.html)
app.mount(
    "/pages",
    StaticFiles(directory=FRONTEND_DIR / "pages"),
    name="pages"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все источники (только для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (включая OPTIONS)
    allow_headers=["*"],
)

# Dependency для получения сессии
async def get_session():
    async with session_maker() as session:
        yield session

@app.post("/send_data")
async def send_data(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    data = await request.json()
    ic(data)
    
    # Добавляем пользователя в БД
    await orm_add_user(session, data)
    return {"status": "success", "data": data}

@app.get("/get_data")  # Лучше использовать GET для получения данных
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await orm_get_users(session)
    ic(users)
    return {"users": users}