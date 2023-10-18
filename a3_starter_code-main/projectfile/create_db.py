<<<<<<< HEAD
from website import db, create_app
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
quit()
=======
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
>>>>>>> 7633c11d1958848b3622133a65f2fd56c11e7f08
