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

class Calc_date(dt.date):
    def is_holiday(self):
        """Определяет является ли дата праздничным днем"""
        holiday = filter(
            lambda val: self.month == val['month'] and self.day in val['day'], HOLIDAYS
        )
        return (len(list(holiday)) != 0)

class Calc_month:
    def __init__(self, year, month, day):
        """
        Инициализация расчетного месяца
        Параметры
        year (int)
        month (int, int) Кортеж из 2 элементов номер месяца и количество дней
        day (int, int) Кортеж из 2 элементов начало и конец периода
        """
        self.norm_days = 0
        self.working_days = 0
        self.month = month[0]

        p = 0  # Переносы выходных дней
        for d in range(1, month[1]+1):
            current_day = Calc_date(year=year, month=self.month, day=d)
            if current_day.weekday() in (5, 6) and current_day.is_holiday():
                p += 1
            elif current_day.weekday() not in (5, 6) and not current_day.is_holiday():
                if p == 0:
                    self.norm_days += 1
                    if day[1] >= d >= day[0]:
                        self.working_days += 1
                else:
                    p -= 1

    def calculate(self, base_pay):
        if self.norm_days == 0:
            return 0
        elif self.working_days == self.norm_days:
            return base_pay
        else:
            return base_pay*self.working_days/self.norm_days

def is_leap(year):
    """Функция определяет является ли год високосным."""
    leap = False
    if year > 0:
        condition01 = (year / 4) == (year // 4)
        condition02 = (year / 100) == (year // 100)
        condition03 = (year / 400) == (year // 400)
        leap = condition03 or condition01 and not condition02

    return leap

def split_period(start_data, end_data):
    """
    Функция разделения периода
    Возвращает список кортежей [(int, [(int, int)])]
    """
    years = [y for y in range(start_data.year, end_data.year+1)]
    months0 = [
        (1, 31), (2, 28), (3, 31), (4, 30), (5, 31), (6, 30), (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31)
    ]
    months1 = [
        (1, 31), (2, 29), (3, 31), (4, 30), (5, 31), (6, 30), (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31)
    ]
    split_period = [(y, months1) if is_leap(y) else (y, months0) for y in years]
    split_period[0] = (split_period[0][0], [m for m in split_period[0][1] if m[0] >= start_data.month])
    split_period[-1] = (split_period[-1][0], [m for m in split_period[-1][1] if m[0] <= end_data.month])

    return split_period

"""
Алгоритм расчета зарплаты
0. Каждому сотруднику назначен оклад (О)
1. Зарплата рассчитывается помесячно
2. Для каждого месяца определяется норма дней (НД) и отработанные дни (ОД)
3. Результат расчета О * ОД / НД с округлением до 2 цифр после запятой
4. Расчет упрощенный, при совпадении праздника и выходного дня
   выходной день переносится на следующий рабочий.
"""
def calcilate_salary(person, start_data, end_data):
    base_pay = person['base_pay']
    sp = split_period(start_data, end_data)

    calculated_months = []
    for year, months in sp:
        for month in months:
            if year == start_data.year == end_data.year and month[0]==start_data.month == end_data.month:
               calculated_months.append(
                    Calc_month(year, month, (start_data.day, end_data.day))
                )
            elif year == start_data.year and month[0] == start_data.month:
                calculated_months.append(
                   Calc_month(year, month, (start_data.day, month[1]))
                )
            elif year == end_data.year and month[0] == end_data.month:
                calculated_months.append(
                    Calc_month(year, month, (1, end_data.day))
                )
            else:
                calculated_months.append(
                    Calc_month(year, month, (1, month[1]))
                )

    return sum(
        [calc_month.calculate(base_pay) for calc_month in calculated_months]
    )
