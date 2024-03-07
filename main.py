import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

#--------------------------ALL FROM WTF SITE--------------------------------
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google maps (URL)', validators=[DataRequired(), URL(message="Enter a valid URL")])
    open = StringField('Opening Times (e.g. 8AM)', validators=[DataRequired()])
    close = StringField('Closing Times (e.g. 9PM)', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'])
    wifi = SelectField('Wifi Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power = SelectField('Power Rating', choices=['✘', '🔋', '🔋🔋', '🔋🔋🔋', '🔋🔋🔋🔋', '🔋🔋🔋🔋🔋'])
    submit = SubmitField('Submit')


#----------------------all Flask routes below--------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():  # POST Method
        with open("cafe-data.csv", "a", encoding="utf-8") as file:
            file.write(f"\n{form.cafe.data},{form.location.data},{form.open.data},{form.close.data}, {form.coffee.data}, {form.wifi.data}, {form.power.data}")
        return redirect(url_for('cafes'))
    else:
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        length = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, length=length)



if __name__ == '__main__':
    app.run(debug=True)
