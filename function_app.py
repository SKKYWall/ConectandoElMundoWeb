import azure.functions as func
import logging
from openai import OpenAI 

#{"model": "gpt-3.5-turbo", "prompt": "Write a story about an alien and a human astronaut", "max_tokens": 100, "temperature": 1}
secret_key = ""

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="firstfuncapi")
def firstfuncapi(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="completionAPI", auth_level=func.AuthLevel.ANONYMOUS)
def completionAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    
    client = OpenAI(
    api_key=secret_key
    )

    req_body = req.get_json()

    completion = client.chat.completions.create(
        model=req_body["model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": req_body["prompt"]}
        ],
        max_tokens=req_body["max_tokens"],
        temperature=req_body["temperature"]
        )

    return func.HttpResponse(completion.choices[0].message.content, status_code=200)

@app.route(route="imagefunc", auth_level=func.AuthLevel.ANONYMOUS)
def imagefunc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    client = OpenAI(api_key=secret_key,)
    completion = client.images.generate(
    model="dall-e-3",
    prompt=req_body["prompt"],
    n=1,
    size="1024x1024"
)


    return func.HttpResponse(
        completion.data[0].url,
        status_code=200
        )