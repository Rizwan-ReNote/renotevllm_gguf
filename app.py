import ollama
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/ask-image/")
async def ask_image(
    file: UploadFile = File(None),  
    question: str = Form(...)
):

    try:

        image_data = None
        
        if file:
            image_data = file.file.read()
            
        messages = [{'role': 'user', 'content': question}]
        
        if image_data:
            messages[0]['images'] = [image_data]    

        res = ollama.chat(
            model="aiden_lu/minicpm-v2.6:Q4_K_M",
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
