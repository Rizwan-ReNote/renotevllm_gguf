import ollama
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/ask-image/")
async def ask_image(
    file: UploadFile = File(...),
    question: str = Form(...)
):

    try:

        image_data = file.file.read()

        res = ollama.chat(
            model="hf.co/openbmb/MiniCPM-V-2_6-gguf : IQ3",
            messages=[
                {
                    'role': 'user',
                    'content': question,
                    # Pass the image data (binary content)
                    'images': [image_data]
                }
            ]
        )

        # Return the response content from the model
        return JSONResponse(content={"response": res['message']['content']})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
