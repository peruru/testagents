from fastapi import FastAPI, Request

import uuid
from datetime import datetime, timezone

app = FastAPI()


# -----------------------------
# Weather Agent Logic
# -----------------------------
def weather_controller(text: str):

    text_lower = text.lower()

    if "weather" in text_lower and "london" in text_lower:
        return "Weather in London: 12°C, cloudy with light winds."

    elif "weather" in text_lower and "paris" in text_lower:
        return "Weather in Paris: 15°C, partly sunny."

    elif "forecast" in text_lower:
        return "3-Day Forecast: Day1: 15°C Cloudy | Day2: 18°C Sunny | Day3: 16°C Rain."

    elif "temperature" in text_lower:
        return "Current temperature is approximately 22°C."

    elif "hyd" in text_lower or "hyderabad" in text_lower:
        return "Weather in Hyderabad: 30°C, sunny with light breeze."

    return f"WeatherAgent received: {text}"


# -----------------------------
# Agent Card
# -----------------------------
@app.get("/.well-known/agent-card.json")
async def agent_card():
    return {
        "name": "Weather Insight Agent",
        "description": "AI agent that provides weather information and forecasts.",
        "url": "https://eupcfvwitm.us-east-1.awsapprunner.com",
        "version": "1.0.0",
        "rpcEndpoint": "https://eupcfvwitm.us-east-1.awsapprunner.com/rpc",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
            "stateTransitionHistory": False
        },
        "skills": [
            {
                "id": "current-weather",
                "name": "Get Current Weather",
                "description": "Returns current weather conditions for a city.",
                "examples": [
                    "What is the weather in London?",
                    "Weather in Paris today"
                ]
            },
            {
                "id": "forecast",
                "name": "Weather Forecast",
                "description": "Provides upcoming weather predictions.",
                "examples": [
                    "Weather forecast for next 3 days",
                    "Will it rain tomorrow?"
                ]
            }
        ]
    }


# -----------------------------
# JSON-RPC Endpoint
# -----------------------------
@app.post("/")
@app.post("/rpc")
async def handle_json_rpc(request: Request):

    body = await request.json()

    try:
        method = body.get("method")

        if method != "message/send":
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "error": {
                    "code": -32601,
                    "message": "Unsupported method"
                }
            }

        message = body["params"]["message"]
        user_input = message["parts"][0]["text"]

        response_text = weather_controller(user_input)

        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "artifacts": [
                    {
                        "artifactId": str(uuid.uuid4()),
                        "name": "Weather Insight Agent",
                        "parts": [
                            {
                                "kind": "text",
                                "text": response_text
                            }
                        ]
                    }
                ],
                "contextId": str(uuid.uuid4()),
                "id": str(uuid.uuid4()),
                "kind": "task",
                "status": {
                    "state": "completed",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        }

    except Exception:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "error": {
                "code": -32602,
                "message": "Invalid request structure"
            }
        }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def home():
    return {"status": "Weather Agent running"}



