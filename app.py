from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "Charizard"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "femiecoker@gmail.com"
app.config["MAIL_PASSWORD"] = "jpsv wwsi vjuq ptxy"

db = SQLAlchemy(app)

mail = Mail(app)



class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    dob = db.Column(db.Date)
    position = db.Column(db.String(80))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        dob = request.form["dob"]
        dob_obj = datetime.strptime(dob, "%Y-%M-%d")
        position = request.form["position"]

        form = Form(first_name=first_name, last_name=last_name, email=email, dob=dob_obj, position=position)
        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission {first_name},\n"\
                       f"To confirm the information we received: {first_name} \n {last_name} \n {dob} \n {position}"\
                       f" If there are any questions or issues please reach out to us."
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash(f"{first_name}, your form was successfully submitted")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)