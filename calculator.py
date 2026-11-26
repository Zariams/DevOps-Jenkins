from datetime import date


def calculate_days(birth_date: date, today: date | None = None) -> int:
    today = today or date.today()
    if birth_date > today:
        raise ValueError('Дата народження не може бути у майбутньому.')
    return (today - birth_date).days
