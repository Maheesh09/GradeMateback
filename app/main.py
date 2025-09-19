from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import student, papers, questions, schemes, subbmissions, answers, upload
from .config import settings

app = FastAPI(title="Hackathon Marking API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(student.router)
app.include_router(papers.router)
app.include_router(questions.router)
app.include_router(schemes.router)
app.include_router(subbmissions.router)
app.include_router(answers.router)
app.include_router(upload.router)

# Optional: on startup you could verify connectivity
# but DO NOT auto-create tables against an existing DB.
