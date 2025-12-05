import argparse
import os
import sys

def parse_line(row, line_no):
    def warn(msg):
        print("ВНИМАНИЕ " + msg)

    for i in range(len(row)):
        row[i] = row[i].strip()

    try:
        year = int(row[0])
        month = int(row[1])
        day = int(row[2])
        hour = int(row[3])
        minute = int(row[4])
        temperature = int(row[5])
    except Exception:
        warn("Строка {} не удалось преобразовать поля в числа -> пропуск Строка {}".format(line_no, row))
        return None

    return {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "temp": temperature,
    }

def year_stats(datas):
    if not datas:
        print("ВНИМАНИЕ Нет данных для обработки")
        return None

    temp_count = 0
    temp_sum = 0

    temp_max = None
    temp_min = None
    temp_avg = None

    for line in datas:
        new_temp = line['temp']
        temp_sum = temp_sum + new_temp
        temp_count = temp_count + 1

        if (temp_min is None) or (new_temp < temp_min):
            temp_min = new_temp

        if (temp_max is None) or (new_temp > temp_max):
            temp_max = new_temp

    temp_avg = temp_sum / temp_count

    return {
        "avg": temp_avg,
        "max": temp_max,
        "min": temp_min
    }

def month_stats(datas, month_filter=None):
    if not datas:
        print("ВНИМАНИЕ Нет данных для обработки")
        return {}

    monthly_data = {}
    
    for line in datas:
        month = line['month']
        if month not in monthly_data:
            monthly_data[month] = []
        monthly_data[month].append(line)

    if month_filter is not None:
        if month_filter in monthly_data:
            monthly_data = {month_filter: monthly_data[month_filter]}
        else:
            print(f"ВНИМАНИЕ Нет данных для месяца {month_filter}")
            return {}

    result = {}
    for month, data in monthly_data.items():
        temp_count = 0
        temp_sum = 0
        temp_max = None
        temp_min = None

        for line in data:
            new_temp = line['temp']
            temp_sum = temp_sum + new_temp
            temp_count = temp_count + 1

            if (temp_min is None) or (new_temp < temp_min):
                temp_min = new_temp

            if (temp_max is None) or (new_temp > temp_max):
                temp_max = new_temp

        temp_avg = temp_sum / temp_count if temp_count > 0 else 0

        result[month] = {
            "avg": temp_avg,
            "max": temp_max,
            "min": temp_min,
            "count": temp_count
        }

    return result

def print_month_stats(month_stats_dict):
    if not month_stats_dict:
        print("Нет данных для отображения")
        return

    for month, stats in sorted(month_stats_dict.items()):
        print(f"================МЕСЯЦ {month:2d}================")
        print(f"СРЕДНЯЯ:      {stats['avg']:.2f}")
        print(f"МАКСИМАЛЬНАЯ: {stats['max']}")
        print(f"МИНИМАЛЬНАЯ:  {stats['min']}")
        print(f"КОЛИЧЕСТВО:   {stats['count']}")
        print("====================================")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Приложение для вычисления статистики температуры из CSV-файла",
        add_help=False
    )

    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        help="Показать справку по использованию программы"
    )

    parser.add_argument(
        "-f",
        "--file",
        help="Входной CSV-файл",
        required=False
    )

    parser.add_argument(
        "-m",
        "--month",
        type=int,
        help="Номер месяца (1..12) для вывода статистики только по нему",
        required=False
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        print()
        parser.print_help()
        print()
        print("Примеры использования")
        print("  python parser.py -f temperature_big.csv")
        print("  python parser.py -f temperature_big.csv -m 1")
        return

    if args.help:
        parser.print_help()
        print()
        print("Примеры использования")
        print("  python parser.py -f temperature_big.csv")
        print("  python parser.py -f temperature_big.csv -m 1")
        return

    if args.file is None:
        parser.print_help()
        print()
        print("Примеры использования")
        print("  python parser.py -f temperature_big.csv")
        print("  python parser.py -f temperature_big.csv -m 1")
        return

    filename = args.file
    month_filter = args.month

    if not os.path.exists(filename):
        print(f"ОШИБКА Файл '{filename}' не найден")
        print("Убедитесь что файл находится в той же папке что и скрипт")
        return

    if month_filter is not None:
        if not (1 <= month_filter <= 12):
            print("ОШИБКА номер месяца должен быть от 1 до 12")
            return

    print(f"Чтение файла {filename}")
    line_datas = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            line_number = 0
            for line in f:
                line_number += 1
                line = line.strip()

                if line == "":
                    continue

                row = line.split(";")
                if len(row) < 6:
                    print(f"ВНИМАНИЕ Строка {line_number} недостаточно данных -> пропуск")
                    continue
                    
                line_data = parse_line(row, line_number)
                if line_data is not None:
                    line_datas.append(line_data)

        print(f"Успешно обработано строк {len(line_datas)}")

        if not line_datas:
            print("Нет данных для анализа")
            return

        if month_filter is not None:
            monthly_stats = month_stats(line_datas, month_filter)
            if monthly_stats:
                print(f"\nСТАТИСТИКА ЗА МЕСЯЦ {month_filter}")
                print_month_stats(monthly_stats)
        else:
            monthly_stats = month_stats(line_datas)
            if monthly_stats:
                print("\nСТАТИСТИКА ПО МЕСЯЦАМ")
                print_month_stats(monthly_stats)
                
                year_data = year_stats(line_datas)
                if year_data:
                    print("================ГОД=================")
                    print(f"СРЕДНЯЯ:      {year_data['avg']:.2f}")
                    print(f"МАКСИМАЛЬНАЯ: {year_data['max']}")
                    print(f"МИНИМАЛЬНАЯ:  {year_data['min']}")
                    print("====================================")

    except Exception as e:
        print(f"ОШИБКА при чтении файла {e}")
        print("Проверьте правильность формата файла")

if __name__ == "__main__":
    main()