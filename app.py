from flask import Flask, render_template


def create_app():
    from team.sqlitebp import bp as sqlitebp
    from team.mariabp import bp as mariabp
    from team.mongobp import bp as mongobp

    app = Flask(__name__)
    bps = [
        ["SQLite", sqlitebp],
        ["MariaDB", mariabp],
        ["MongoDB", mongobp],
    ]
    bps = sorted(bps)
    for i, (title, bp) in enumerate(bps, start=1):
        app.register_blueprint(bp, url_prefix=f"/{i}")

    @app.route("/")
    def index():
        return render_template("index.tpl", bps=bps)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
