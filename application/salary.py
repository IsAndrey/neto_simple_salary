"""Модуль расчета зарплаты."""
import datetime as dt


HOLIDAYS = [
    {'month': 1, 'day': (1, 2, 3, 4, 5, 6, 7, 8)},
    {'month': 2, 'day': (23,)},
    {'month': 3, 'day': (8,)},
    {'month': 5, 'day': (1, 9)},
    {'month': 6, 'day': (12,)},
    {'month': 11, 'day': (4,)}
]

class calc_date(dt.date):
    def is_holiday(self):
        holiday = filter(
            lambda val: self.month == val['month'] and self.day in val['day'], HOLIDAYS
        )
        return (len(list(holiday)) == 1)

class calc_month:
    def __init__(self, year, month, day):
        self.norm_days = 0
        self.working_days = 0
        self.month = month
        one_day = dt.timedelta(days=1)
        current_day = calc_date(year=year, month=month, day=1)
        while current_day.month == self.month:
            if current_day.weekday() not in (5, 6) and not current_day.is_holiday():
                self.norm_days += 1
                if current_day.day >= day:
                    self.working_days += 1
            current_day += one_day

    def calculate(self, base_pay, accuracy=2):
        if self.norm_days == 0:
            return 0
        else:
            return round(base_pay*self.working_days/self.norm_days, accuracy)


def calcilate_salary(person, start_data, end_data):
    base_pay = person['base_pay']
    one_day = dt.timedelta(days=1)
    current_data = calc_date(
        year=start_data.year, month=start_data.month, day=start_data.day
    )
    calculated_monthes = [
        calc_month(
            year=current_data.year, month=current_data.month, day=current_data.day
        )
    ]
    while current_data <= end_data:
        if current_data.month != calculated_monthes[-1].month:
            calculated_monthes.append(
                calc_month(
                    year=current_data.year, month=current_data.month, day=current_data.day
                )
            )
        current_data += one_day
    
    return sum(
        [month.calculate(base_pay, 5) for month in calculated_monthes]
    )
