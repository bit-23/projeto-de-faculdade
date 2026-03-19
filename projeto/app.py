from flask import Flask

app=Flask(__name__)

from views import *

if __name__ == "__name__":
    app.run()

