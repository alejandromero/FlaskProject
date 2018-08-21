from app import app

app.jinja_env.globals.update(len=len)
app.jinja_env.globals.update(range=range)