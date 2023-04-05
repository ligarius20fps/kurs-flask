z = set()
z.add(3)
z.update([1,2])
z2 = {2,5,False}

print(z.union(z2))
print(z.symmetric_difference(z2))
print(z.intersection(z2))

number = int(input('dej liczba: '))
if number in range(10):
    print(f'liczba {number} jest w zbiorze')
elif number < 0:
    print(f'liczba {number} znajduje się poniżej zbioru')
else:
    print(f'liczba {number} znajduje się powyżej zbioru')