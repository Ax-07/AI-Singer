from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import RenderRequest, RenderResponse
from .singer_engine import render_singer_fake
from .audio_utils import save_wave

app = FastAPI()

# CORS pour que ton front React (localhost:3000 par ex.) puisse appeler l’API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Singer proto API"}


@app.post("/render-voice", response_model=RenderResponse)
def render_voice(req: RenderRequest):
    audio = render_singer_fake(req)
    filename = "rendered_clip.wav"

    rel_path = save_wave(audio, req.sample_rate, filename)
    duration = len(audio) / req.sample_rate

    return RenderResponse(
        audio_url=rel_path,
        duration=duration,
    )
