"""Модуль управления перноналом."""


def get_employeers():
    """Получение списка сотрудников."""
    data = [
        {'id': '00001', 'full_name': 'Иван Иванович Иванов', 'position': 'Генеральный директор', 'base_pay': 200},
        {'id': '00002', 'full_name': 'Афанасий Борщев', 'position': 'Сантехник', 'base_pay': 50},
        {'id': '00003', 'full_name': 'Федул', 'position': 'Грузчик', 'base_pay': 30},
        {'id': '00004', 'full_name': 'Катя Снегирева', 'position': 'Медсестра', 'base_pay': 75},
        {'id': '00005', 'full_name': 'Коля', 'position': 'Штукатур', 'base_pay': 60},
    ]
    return data