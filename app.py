import ollama
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/ask-image/")
async def ask_image(
    file: UploadFile = File(None),
    question: str = Form(...),
):

    try:
        if file:
            image_data = file.file.read()
        else:
            image_data = None

        res = ollama.chat(
            model="aiden_lu/minicpm-v2.6:Q4_K_M",
            messages=[
                {
                    'role': 'user',
                    'content': question,
                    'images': [image_data] if image_data else None
                }
            ],
             temperature=0.1,
             top_p=0.9,           # Adjusts the diversity of the model's responses.
             max_tokens=150,      # Limits the length of the generated output.
             presence_penalty=0.6, # Encourages variety in the content.
             frequency_penalty=0.5 # Reduces repetition in the output.
        )

        return JSONResponse(content={"response": res['message']['content']})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
