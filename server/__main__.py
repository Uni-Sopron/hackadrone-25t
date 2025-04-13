from flask_openapi3.models.info import Info
from flask_openapi3.models.server import Server
from flask_openapi3.openapi import OpenAPI

from .api import api
from .admin import admin

SERVER_DOMAIN = "127.0.0.1"
SERVER_PORT = 5000

info = Info(title="HackaDrone API", version="0.1")
servers = [
    Server(
        url=f"https://{SERVER_DOMAIN}:{SERVER_PORT}", description="HackaDrone server"
    )
]
app = OpenAPI("HackaDrone server", info=info, servers=servers)

app.register_api(api)
app.register_api(admin)

print("Server is running...")
app.run(host="0.0.0.0", port=SERVER_PORT, ssl_context="adhoc")
