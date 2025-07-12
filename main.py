from fastapi import FastAPI
from routes import user_routes, question_routes, answer_routes

app = FastAPI(title="StackIt - Minimal Q&A Platform")

# Include routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(question_routes.router, prefix="/questions", tags=["Questions"])
app.include_router(answer_routes.router, prefix="/answers", tags=["Answers"])

@app.get("/")
def root():
    return {"message": "Welcome to StackIt API"}