import datetime
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
holidays = []
attendance = {}
leaves = {}
semester_start = datetime.date(year=2022, month=1, day=1)
semester_end = datetime.date(year=2022, month=5, day=31)
semester_days = (semester_end - semester_start).days + 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    date = request.form['date']
    holidays.append(datetime.strptime(date, '%Y-%m-%d').date())
    return 'Holiday added on {}'.format(date)

@app.route('/mark_leave', methods=['POST'])
def mark_leave():
    name = request.form['name']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    leaves[name] = leaves.get(name, []) + [date]
    return 'Leave marked for {} on {}'.format(name, date)

@app.route('/attendance')
def view_attendance():
    name = request.args.get('name')
    if name not in attendance:
        return 'No attendance data found for {}'.format(name)
    attendance_dates = attendance[name]
    total_days = (max(attendance_dates) - min(attendance_dates)).days + 1
    working_days = len([date for date in attendance_dates if date not in holidays])
    leave_days = len(leaves.get(name, []))
    attendance_percentage = ((working_days - leave_days) / total_days) * 100
    remaining_holidays = len([date for date in holidays if min(attendance_dates) <= date <= max(attendance_dates)])
    return jsonify(attendance_percentage=attendance_percentage, remaining_holidays=remaining_holidays)

if __name__ == '__main__':
    app.run()