from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI Client
client = openai.OpenAI(
    api_key=os.getenv("NEXUS_API_KEY"),
    base_url="https://apidev.navigatelabsai.com"
)

# Request Model
class PromptRequest(BaseModel):
    user_prompt: str

# Health Route
@app.get("/")
def root():
    return {"message": "NexusAI Backend Running"}

# Main Route
@app.post("/run_task/")
async def run_task(req: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are a personal AI tutor."
                },
                {
                    "role": "user",
                    "content": req.user_prompt
                }
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}