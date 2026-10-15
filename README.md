#About
This is an localhosted ollama fastapi server that works on your computer using the local cpu and gpu for the computation and answering.

@How it works?
In order to make it work first you need to have a running server of any local hosted ollama using the command.
```bash
ollama run llama3.2:XX
```
After having a running server run the fastapi request using the command.
```bash
uvicorn main:app --reload
```
In this you get server ready on the ```http://127.0.0.1:8000``` or on the ```http://localhost:11434```.

#Why building it?
We have implemented the /POST request and GET /health request using the local hosted model.
Which provide us a health check through status as 'OK' on the page itself.
We also can see the message responnse of the model using the local host model under the /POST tab on the page ```http://127.0.0.1:8000/docs``` and on expanding it you get the try it out button after that use execute.
# Ollama FastAPI Server

A small FastAPI service that sits in front of a locally running Ollama model.
Callers send a message to this service's `/chat` endpoint and get the model's
reply back, without needing to know how Ollama works underneath.

## How it fits together

There are two separate servers here:

```
caller  --->  FastAPI service (this repo)  --->  Ollama server  --->  model
              http://127.0.0.1:8000                http://localhost:11434
```

- **Ollama** (port 11434) runs the model. It is installed separately.
- **This service** (port 8000) is a thin layer in front of it. It defines its
  own request and response format and reports whether Ollama is reachable.

Callers only depend on this service's format, so the model behind it can be
swapped later without changing the callers.

## Setup

1. Install [Ollama](https://ollama.com/) and download the model:
   ```bash
   ollama pull llama3.2:1b
   ```
   Ollama runs in the background after installation. If it is not running,
   start it with `ollama serve`.

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1      # PowerShell
   pip install -r requirements.txt
   ```

## Run

```bash
uvicorn main:app --reload
```

The service starts on `http://127.0.0.1:8000`. Interactive docs are at
`http://127.0.0.1:8000/docs`: expand `POST /chat`, click **Try it out**, edit the
message, and click **Execute**.

The model name is set by `MODEL` at the top of `main.py` (`llama3.2:1b`).

## Endpoints

### `POST /chat`

Request:
```json
{"message": "Say hi in five words."}
```

Response:
```json
{"reply": "Hello, how are you?"}
```

Example:
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Say hi in five words."}'
```

A request without a string `message` is rejected automatically. If Ollama
fails during a request, the service returns `502`.

### `GET /health`

Returns `{"status": "ok"}` with status `200` when Ollama is reachable, and
status `503` when it is not. This is the kind of endpoint tools like Docker and
Kubernetes call to decide whether a service is working.

## Limits

- **Stateless:** each request is independent. The model does not remember
  earlier messages unless they are included in the request.
- **Small model:** `llama3.2:1b` answers quickly but can be wrong, including
  on simple arithmetic, and is unreliable at tool calling.
- **Slow first request:** the first call after Ollama has been idle can take
  15 to 20 seconds while the model loads into memory.
- **Shallow health check:** `/health` confirms the Ollama server is reachable,
  not that the model can generate a reply.
