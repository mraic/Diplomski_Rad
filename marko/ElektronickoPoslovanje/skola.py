igra = input('Želite li igrati (da/ne): \n')

while igra == 'da':

    odabir = input('Gdje želite ići, lijevo ili desno (lijevo/desno): \n')
    hp = 10
    print('Imate',hp,'HP')

    if odabir == 'lijevo':
        hp = hp - 5
        print('Došli ste na livadu gdje vas je ubola pčela, i izgubili ste 5 HP. Sada imate',hp, 'HP\n')
        odabir2 = input('Gdje želite ići? (jezero/ rijeka): \n')

        if odabir2 == 'jezero':
            hp = hp - 5
            print('Napala vas je riba i izgubili ste 5HP.Preostalo vam je',hp,' HP\n')

            if hp <= 0:
                exit
                print('Igra je gotova\n')
                igra = input('Želite li ponovno igrati (da/ne): \n')
                

    

    elif odabir == 'desno':
        print('Odaberite lijevo / desno \n')
        hp = hp -5
        print('Dosli ste na planinu. Napao vas je medvjed i izgubili ste 5 HP. Sada imate',hp ,'HP\n')
        odabir3 = input('Gdje želite ići? (pećina/ koliba): ')

        if odabir3 == 'pećina':
            hp = hp - 5
            print('Napao vas je medvjed i izgubili ste 5HP.Preostalo vam je', hp,HP)

            if hp == 0:
                exit
                print('Igra je gotova')
                igra = input('Želite li igrati ponovno(da/ne): ')
        
        elif odabir3 == 'koliba':
            hp = hp + 3
            print('Čestitamo, pobijedili ste sa',hp,'HP')