import gevent.monkey
gevent.monkey.patch_all()

import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/test'
db = SQLAlchemy(app)

@app.route('/')
def index():
    for i in range(10):
        db.session.execute('SELECT SLEEP(0.1)')
    db.session.commit()
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)
