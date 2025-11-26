string = "abracadabraaaa"
slovar = {} 

for char in string:
    # get возвращает значение ключа, если ключ есть в словаре, иначе 0.
    slovar[char] = slovar.get(char, 0) + 1

print(slovar)
