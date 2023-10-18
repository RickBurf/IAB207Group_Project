from website import db, create_app
from website.models import *
app = create_app()
print("App created")
ctx = app.app_context()
print("App context created")
ctx.push()
print("Context pushed")
db.create_all()
print("Database tables created")