import ollama
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

Prompt = '''Please analyze the provided image and extract all text as it appears, including Arabic script, any other languages, and symbols. Pay close attention to the Arabic text, ensuring that all details such as diacritics, ligatures, and the connected nature of Arabic letters are captured. Return the text exactly as it is written in the image, without translation, interpretation, or any additional information.'''

@app.post("/Ar_OCR/")
async def ask_image(
    file: UploadFile = File(...)
    # question: str = Form(Prompt),
):

    try:
        # Read the image data
        image_data = file.file.read()

        # Perform OCR using the specified question prompt
        res = ollama.chat(
            model="minicpm-v:latest",
            messages=[
                {
                    'role': 'user',
                    'content': Prompt,
                    'images': [image_data]
                }
            ]
        )

        return JSONResponse(content={"text": res['message']['content']})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



# import os
# import ollama
# from fastapi import FastAPI, File, Form, UploadFile
# from fastapi.responses import JSONResponse

# # Step 1: Set environment variables if the ollama API supports them (Optional)
# os.environ["OLLAMA_TEMPERATURE"] = "0.1"
# os.environ["OLLAMA_TOP_P"] = "0.9"
# os.environ["OLLAMA_MAX_TOKENS"] = "150"
# os.environ["OLLAMA_PRESENCE_PENALTY"] = "0.6"
# os.environ["OLLAMA_FREQUENCY_PENALTY"] = "0.5"

# app = FastAPI()

# @app.post("/ask-image/")
# async def ask_image(
#     file: UploadFile = File(None),
#     question: str = Form(...),
# ):
#     try:
#         # Read image data if provided
#         image_data = file.file.read() if file else None

#         # Step 2: Attempt to use model configuration if available
#         # Some APIs might allow configuring the model at load time
#         model_name = "aiden_lu/minicpm-v2.6:Q4_K_M"
#         model_config = {
#             "temperature": 0.1,
#             "top_p": 0.9,
#             "max_tokens": 150,
#             "presence_penalty": 0.6,
#             "frequency_penalty": 0.5
#         }

#         try:
#             # Attempt to load with configuration (if supported)
#             model = ollama.load_model(model_name, config=model_config)
#         except AttributeError:
#             # Fallback if load_model or config isn’t supported
#             model = model_name  # Just use the model name

#         # Step 3: Call the chat function without unsupported parameters
#         res = ollama.chat(
#             model=model,
#             messages=[
#                 {
#                     'role': 'user',
#                     'content': question,
#                     'images': [image_data] if image_data else None
#                 }
#             ]
#             # Avoid adding unsupported parameters here
#         )

#         # Extract response content from the result
#         return JSONResponse(content={"response": res['message']['content']})

#     except Exception as e:
#         # Return an error response if anything fails
#         return JSONResponse(content={"error": str(e)}, status_code=500)
