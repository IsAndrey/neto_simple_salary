import datetime as dt
from application import *

def calculation01():
    staff_data = get_employeers()
    start_data = dt.date(year=2025, month=3, day=1)
    end_data = dt.date(year=2025, month=3, day=15)
    if len(staff_data) > 0:
        print('calculating 1 ...')
        for row in staff_data:
            row['result'] = '{:.2f}'.format(
                calcilate_salary(person=row, start_data=start_data, end_data=end_data)
            )
        print('creating pdf file ... output01.pdf')
        table_header = ['Табельный номер', 'Фамилия, Имя, Отчетство', 'Должность', 'Оклад', 'Аванс']
        table_rows = [[v for v in row.values()] for row in staff_data]
        params = {
            'title': 'Аванс по заработной плате за март 2025 года.',
            'barcode_data': '012345678',
            'table_header': table_header,
            'table_rows': table_rows,
            'output': 'output01.pdf'
        }
        create_pdf(**params)

def calculation02():
    staff_data = get_employeers()
    start_data = dt.date(year=2025, month=1, day=1)
    end_data = dt.date(year=2027, month=12, day=31)
    if len(staff_data) > 0:
        print('calculating 2 ...')
        for row in staff_data:
            row['result'] = '{:.2f}'.format(
                calcilate_salary(person=row, start_data=start_data, end_data=end_data)
            )
        print('creating pdf file ... output02.pdf')
        table_header = ['Табельный номер', 'Фамилия, Имя, Отчетство', 'Должность', 'Оклад', 'Запранировано']
        table_rows = [[v for v in row.values()] for row in staff_data]
        params = {
            'title': 'Среднесрочный план по заработной плате на 2025-2030 года.',
            'barcode_data': '012345678',
            'table_header': table_header,
            'table_rows': table_rows,
            'output': 'output02.pdf'
        }
        create_pdf(**params)

def calculation03():
    staff_data = get_employeers()[1:3]
    start_data = dt.date(year=2025, month=3, day=6)
    end_data = dt.date(year=2025, month=3, day=12)
    if len(staff_data) > 0:
        print('calculating 3 ...')
        for row in staff_data:
            row['result'] = '{:.2f}'.format(
                calcilate_salary(person=row, start_data=start_data, end_data=end_data)
            )
        print('creating pdf file ... output03.pdf')
        table_header = ['Табельный номер', 'Фамилия, Имя, Отчетство', 'Должность', 'Оклад', 'К удержанию']
        table_rows = [[v for v in row.values()] for row in staff_data]
        params = {
            'title': 'Расчет удержанной заработной платы сотрудников с 06.03.2025 по 12.03.2025.',
            'barcode_data': '012345678',
            'table_header': table_header,
            'table_rows': table_rows,
            'output': 'output03.pdf'
        }
        create_pdf(**params)

if __name__ == '__main__':
    print(dt.date.today())
    calculation01()
    calculation02()
    calculation03()
