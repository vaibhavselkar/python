import re
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from spellchecker import SpellChecker

app = FastAPI()
spell = SpellChecker()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the Feedback API!"}

@app.post("/feedback")
async def feedback(request: Request):
    try:
        data = await request.json()
        if "feedback" not in data or not isinstance(data["feedback"], str):
            return JSONResponse(
                {"error": "Invalid input, please provide 'feedback' as a string"},
                status_code=400,
            )

        feedback_text = data["feedback"]
        feedback_cleaned = re.sub("[^A-Za-z0-9 ]+", "", feedback_text)
        words = feedback_cleaned.split()
        misspelled = spell.unknown(words)

        corrections = {word: spell.correction(word) for word in misspelled}

        return JSONResponse(
            {
                "Original Feedback": feedback_text,
                "Corrections": corrections,
            }
        )
    except Exception as e:
        return JSONResponse(content={"error": f"Internal error: {str(e)}"}, status_code=500)
