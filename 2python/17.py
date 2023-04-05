from random import randint

odp = input('Czy masz ochotę zagrać w grę? ').lower()
while odp in {'dobra', 'tak', 'ok', 't', 'y', 'yes'}:
    magic = randint(1,5)
    odp = int(input('Wylosowałem liczbę od 1 do 5\nZgadnij jaką '))
    if odp == magic:
        print('ŁOOO ZGADŁÆŚ :D')
    elif odp not in range(1,5):
        print('Przecież wyraźnie napisałem, że wylosowałem liczbę od 1 do 5 a ty mi dałæś spoza tego przedziału!')
    elif abs(odp-magic) == 1:
        print(f'Aj, było blisko, chodziło o {magic}')
    elif abs(odp-magic) == 2:
        print(f'Mogłem się spodziewać, że nie trafisz, bo chodziło o {magic} {magic}')
    elif abs(odp-magic) == 3:
        print(f'Pudło, chodziło o {magic}')
    else:
        print(f'Trzeba było spróbować z drugiego końca, chodziło o {magic}')
    odp = input('Chcesz jeszcze raz zagrać? ').lower()
