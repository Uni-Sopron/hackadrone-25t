import os

from flask_openapi3.models.info import Info
from flask_openapi3.models.server import Server
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.types import SecuritySchemesDict

from .api import api
from .admin import admin

SERVER_URL = os.getenv("SERVER_URL", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))

api_key = {
  "type": "apiKey",
  "name": "Api-Key",
  "in": "header"
}
security_schemes: SecuritySchemesDict = {"Api-Key": api_key}

info = Info(title="HackaDrone API", version="0.1")
servers = [
    Server(
        url=f"https://{SERVER_URL}:{SERVER_PORT}", description="HackaDrone server"
    )
]
app = OpenAPI("HackaDrone server", info=info, servers=servers, security_schemes=security_schemes)

app.register_api(api)
app.register_api(admin)

print("Server is running...")
app.run(host="0.0.0.0", port=SERVER_PORT, ssl_context="adhoc")
