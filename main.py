import datetime as dt
from application import create_pdf
from application import get_emploeers
from application import calcilate_salary

if __name__ == '__main__':
    staff_data = get_emploeers()
    # Зарплата за первую половину месяца
    start_data = dt.date(year=2025, month=3, day=10)
    end_data = dt.date(year=2025, month=4, day=30)
    if len(staff_data) > 0:
        table_header = ['Табельный номер', 'Фамилия, Имя, Отчетство', 'Должность', 'Оклад', 'Начислено']
        for row in staff_data:
            row['result'] = calcilate_salary(person=row, start_data=start_data, end_data=end_data)
        print(table_header)
        table_rows = [[v for v in row.values()] for row in staff_data]
        print(table_rows)
        params = {
            'title': 'Отчет по заработной плате.',
            'barcode_data': '012345678',
            'table_header': table_header,
            'table_rows': table_rows,
            'output': 'output01.pdf'
        }
        create_pdf(**params)
