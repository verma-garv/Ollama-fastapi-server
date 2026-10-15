import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health():
    try:
        requests.get(f"{OLLAMA_URL}/api/tags",timeout=2).raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Ollama is not reachable")
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": req.message}],
                "stream": False,
            },
            timeout=120,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ollama request failed: {e}")
    return ChatResponse(reply=r.json()["message"]["content"])
