matrix = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

shift = int(input("Введите величину сдвига: "))

result = [row[-shift:] + row[:-shift] for row in matrix] #матрица из трех строк на вывод, сначала берутся все элементы от
# -shift до конца, затем добавляются элементы от начала до индекса -shift

print("Результат:")
for row in result:
    print(row)