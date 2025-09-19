from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routes import auth, transactions,chatbot,profile,sms,profile_build, goals, issued_batches, streaks, available_badges


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(chatbot.router)
app.include_router(profile.router)
app.include_router(sms.router)
app.include_router(profile_build.router)
app.include_router(goals.router)
app.include_router(issued_batches.router)
app.include_router(streaks.router)
app.include_router(available_badges.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
def startup():
    init_db()