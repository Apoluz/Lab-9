from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для хранения информации о местах работы
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)  # название компании
    term = db.Column(db.Integer, nullable=False)         # срок работы в месяцах

# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        company = request.form.get('company')
        term = request.form.get('term', type=int)

        # Проверяем, что введено название и срок
        if company and term is not None:
            new_job = Job(company=company, term=term)
            db.session.add(new_job)
            db.session.commit()
        return redirect(url_for('index'))

    # Получаем все записи и считаем общий стаж
    jobs = Job.query.all()
    total_months = sum(job.term for job in jobs)
    return render_template('index.html', jobs=jobs, total=total_months)

# Дополнительное задание:
# Очистка ленты сообщений по нажатию кнопки «Очистить»
@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Job).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
