import jwt
import requests
from starlette.status import HTTP_401_UNAUTHORIZED
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
import os
from dotenv import load_dotenv


# region Auth API Key

load_dotenv()

API_KEY = os.environ['MCP_API_KEY']

# endregion

# region Auth Middleware API Key

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log authorization header from the request
        auth_header = request.headers.get("authorization")
        if auth_header:
            logging.info(f"Authorization Header: {API_KEY}")
        # Allow root endpoint without auth
        if request.url.path == "/": 
            return await call_next(request)
        auth_header = request.headers.get("authorization")
        if not auth_header:
            accept = request.headers.get("accept", "")
            if "application/json" in accept:
                return JSONResponse({"error": "🔒 Authentication Failed ⛔"}, status_code=401)
            else:
                return PlainTextResponse("🔒 Authentication Failed ⛔", status_code=401)
        # Check if CLIENT_API_KEY matches API_KEY
        if not API_KEY or not CLIENT_API_KEY:
            accept = request.headers.get("accept", "")
            if "application/json" in accept:
                return JSONResponse({"error": "🔒 Authentication Failed ⛔"}, status_code=401)
            else:
                return PlainTextResponse("🔒 Authentication Failed ⛔", status_code=401)
        if CLIENT_API_KEY != API_KEY:
            accept = request.headers.get("accept", "")
            if "application/json" in accept:
                return JSONResponse({"error": "🔒 Authentication Failed ⛔"}, status_code=401)
            else:
                return PlainTextResponse("🔒 Authentication Failed ⛔", status_code=401)
        # If keys match, authentication succeeds
        return await call_next(request)

# endregion
