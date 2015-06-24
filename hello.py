import os
from flask import Flask
from flask import render_template, request, json
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/test.db')
db = SQLAlchemy(app)

class Entry(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  Fullname = db.Column(db.String(60))
  Email = db.Column(db.String(60), unique=True)

  def __init__(self, Fullname, Email):
    self.Fullname = Fullname
    self.Email = Email

  def __repr__(self):
    return "Informacion de - %s" % self.Fullname

@app.route('/', methods=["GET", "POST"])
def form():
  if request.method == 'GET':
    return render_template('home-fullwidth.html')
  elif request.method == 'POST':
    print 'Es un post'
    args = {}
    # Get form parameters
    getEmail = request.form.get('Email', '')

    print getEmail

    # Anadir la entrada solamente si no existe
    previousEntry = Entry.query.filter_by(Email=getEmail).first()
    if previousEntry is None:
      args["Fullname"] = request.form.get("Fullname", "n/a")
      args["Email"] = request.form.get("Email", "n/a")
    
      entry = Entry(**args)
      db.session.add(entry)
      db.session.commit()

    return render_template("thanks.html")

@app.route('/more-info', methods=["GET", "POST"])
def sponsors():
  if request.method == 'GET':
    return render_template('more-info.html')

if __name__ == '__main__':
	app.run()