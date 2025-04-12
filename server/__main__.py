from flask_openapi3.models.info import Info
from flask_openapi3.openapi import OpenAPI

from .api import api
from .admin import admin

info = Info(title="HackaDrone API", version="0.1")
app = OpenAPI("HackaDrone server", info=info)
app.register_api(api)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
