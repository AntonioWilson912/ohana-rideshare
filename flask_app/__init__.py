from flask import Flask

app = Flask(__name__)
app.secret_key = "a8sdihonqw"

@app.template_filter("strftime")
def _jinja2_filter_datetime(value, format="%B %d, %Y"):
    return value.strftime(format)