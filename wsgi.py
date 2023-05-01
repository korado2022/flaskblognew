from flask import render_template, url_for
from werkzeug.utils import redirect

from blog.app import create_app


app = create_app()


@app.route("/")
def index():
    return redirect(url_for('article.article_list'))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )