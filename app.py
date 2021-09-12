from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# URI needs to start with 'postgresql://' instead of 'postgres://' - which is what Heroku gives you by default in their URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yazvyedzkpranp:0daa57726febcf44fc4f28c603d75773d27cdc4f11c70ec1bc4194bfe9b98943@ec2-44-195-16-34.compute-1.amazonaws.com:5432/dcl8opt0i5ffhv'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# set up database
class Feedback(db.Model):
  __tablename__ = 'feedback'
  id = db.Column(db.Integer, primary_key=True)
  customer = db.Column(db.String(200), unique=True)
  dealer = db.Column(db.String(200))
  rating = db.Column(db.Integer)
  comments = db.Column(db.Text())

  def __init__(self, customer, dealer, rating, comments):
    self.customer = customer
    self.dealer = dealer
    self.rating = rating
    self.comments = comments


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
  if request.method == 'POST':
    customer = request.form['customer']
    dealer = request.form['dealer']
    rating = request.form['rating']
    comments = request.form['comments']
    # print(customer, dealer, rating, comments)
    if customer == '' or dealer == '':
      return render_template('index.html', message='Please enter required fields.')

    if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
      data = Feedback(customer, dealer, rating, comments)
      db.session.add(data)
      db.session.commit()
      return render_template('success.html')
    else:
      return render_template('index.html', message='You have already submitted feedback.')



if __name__ == '__main__':
  app.run()