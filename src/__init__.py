from fastapi import FastAPI, APIRouter
from fastapi.concurrency import asynccontextmanager
from src.db import initdb
from src.user.routes import user_router
from src.chat.routes import Chat_router
from src.messages.routes import Messages_router
from fastapi.middleware.cors import CORSMiddleware
from src.webSocket import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):    
    await initdb()
    yield
    print("server is stopping")

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users")
app.include_router(Messages_router, prefix="/messages")
app.include_router(Chat_router,prefix="/chats")
app.include_router(ws_router)



