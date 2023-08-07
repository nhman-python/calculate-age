import datetime
import os
from flask import Flask, request, render_template, jsonify
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields import DateField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = os.urandom(32)
csrf = CSRFProtect(app)


class BirthdayForm(FlaskForm):
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[InputRequired()])


def calculate_age(birth_date):
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


@app.route('/', methods=['POST', 'GET'])
def index():
    form = BirthdayForm(request.form)
    if request.method == 'POST':
        if form.validate():
            birth_date = form.birth_date.data
            try:
                if birth_date > datetime.date.today():
                    raise ValueError("Oops! You can't be born in the future!")

                age = calculate_age(birth_date)
                seconds_old = (datetime.datetime.now() - datetime.datetime.combine(birth_date, datetime.time.min)).total_seconds()
                days_old = (datetime.date.today() - birth_date).days
                years_old = days_old / 365

                if days_old in [0, 1]:
                    raise ValueError("It looks like you were born today!")

                return jsonify({
                    'seconds': round(seconds_old, 2),
                    'days': round(days_old, 2),
                    'years': round(years_old, 2)
                })
            except ValueError as err:
                return jsonify({'result': f"Error: {err}"})
        else:
            return jsonify({'result': 'Invalid input. Please enter a valid date.'})

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run()
