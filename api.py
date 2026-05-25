import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from main import MarkovChain

app = FastAPI(title= "MarkovChainAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def tokenize(text: str) -> list[str]:
    tokens = []

    for word in text.split():
        clean_word = re.sub(r"^[^\w]+|[^\w]+$", "", word).lower()

        if clean_word:
            tokens.append(clean_word)

    return tokens

class ChatRequest(BaseModel):
    message: str
    length: int = Field(default = 50, ge = 1, le = 200)
    order: int = Field(default = 2, ge = 1, le = 10)
    meaningfulness: float = Field(default=0.7, ge=0.0, le=1.0)

class ChatResponse(BaseModel):
    reply: str
    token_count: int
    order: int

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    training_tokens = tokenize(request.message)

    required_tokens = request.order + 1

    if len(training_tokens) < required_tokens:
        return {"reply": f"Слишком мало текста для генерации. Нужно минимум {required_tokens} слов.",
            "token_count": len(training_tokens),
            "order": request.order}
    
    model = MarkovChain(order = request.order)

    try:
        model.train(training_tokens)
    except ValueError as error:
        return {
            "reply": str(error),
            "token_count": len(training_tokens),
            "order": request.order
    }

    generated_text = model.generate(length=request.length, meaningfulness=request.meaningfulness)

    return {
        "reply": generated_text,
        "token_count": len(training_tokens),
        "order": request.order
    }


