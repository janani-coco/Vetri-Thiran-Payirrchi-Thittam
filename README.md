# ComicCraft — AI Comic Story Creator

A FastAPI + Jinja2 application that creates a five-panel comic outline and script with Gemini, illustrates each panel, previews it in the browser, and exports a PDF. The interface and API follow the supplied project brief.

## Requirements
- Python 3.10 or 3.11 recommended.
- A Gemini API key for real outline/script generation.
- Optional: a capable GPU and the optional Diffusers dependencies for local Stable Diffusion. CPU image generation is possible but very slow and memory-intensive.

The brief names Gemini 1.5 and an older Google SDK. This implementation uses Google's current `google-genai` SDK and configurable model IDs instead; check the current [Gemini model list](https://ai.google.dev/gemini-api/docs/models). Hugging Face Diffusers is an optional local image backend; the default placeholder backend lets you validate the app without downloading model weights.

## VS Code setup
1. Unzip the project and open the `comiccraft` folder in VS Code.
2. Install the Microsoft Python extension.
3. Open **Terminal → New Terminal** in the project root.
4. Create and activate an environment:

   **Windows PowerShell**
   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
5. Install packages:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. Copy `.env.example` to `.env`, then add your Gemini API key. Keep `.env` private and never commit it.

## Run
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs.

## Image generation options
- **Quick UI test:** leave `IMAGE_PROVIDER=placeholder`. This produces demo art locally; Gemini still needs a key to generate story content.
- **Real Stable Diffusion:** install PyTorch appropriate for your operating system/GPU first (see [PyTorch install selector](https://pytorch.org/get-started/locally/)), then `pip install -r requirements-image.txt`. Set `IMAGE_PROVIDER=diffusers` in `.env`. The first generation downloads model weights and can take time. Confirm the model's license and access terms before use.

## API and smoke tests
Interactive docs at `/docs` expose:
- `POST /generate-comic/json` — JSON comic generation.
- `POST /test-image` — standalone image test using form field `prompt`.
- `GET /download/{filename}` — retrieve a generated PDF.

Example JSON body:
```json
{
  "prompt": "A brave fox finds a lost star and returns it to the night sky",
  "character_name": "Pip",
  "setting": "An enchanted forest",
  "tone": "light-hearted",
  "art_style": "comic book"
}
```

Basic health check:
```bash
curl -i http://127.0.0.1:8000/
```
It should return HTTP 200 and the ComicCraft homepage. For full generation, use a valid Gemini key, then submit the form or call the JSON endpoint. PDF links are returned as `pdf_url` by the API.

## Project structure
```text
comiccraft/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routes.py
│   ├── schemas.py
│   └── services/
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── style.css
│   ├── panels/
│   └── exports/
├── tests/
├── .env.example
├── requirements.txt
└── requirements-image.txt
```

## Troubleshooting
- `GEMINI_API_KEY is missing`: copy `.env.example` to `.env` and set a valid key.
- Model not found/access denied: set `GEMINI_OUTLINE_MODEL` and `GEMINI_STORY_MODEL` to model IDs enabled for your API key.
- Diffusers install fails: install PyTorch separately using the official selector, then install the optional requirements. Avoid mixing CPU and CUDA wheels.
- Generation timeout: local image inference can take minutes; try fewer `IMAGE_STEPS`, or use the placeholder backend while developing.
