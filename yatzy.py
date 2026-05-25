import random

## HJÄLPFUNKTIONER OCH VALIDERING
def frekvenskarta(tarningar):
    """
    Räknar  och visar hur många av varje tärningsvärdesom finns(1-6).
    """
    print("\nfrekvenskarta för tärningarna:" )
    for i in range(1, 7):
        antal = tarningar.count(i)
        print(f"Tärning {i}: {antal} st")

def validerahamta_index():
    """
    Hämtar samt validerar indexmatningen från spelet. 
    Ser till att index är heltal mellan 0 till 4, unika och förhindrar krascher.
    Koden kraschar inte om spelaren råkar skriva bokstäver.
    """
    while True:
        try:
            print("Ange index(0-4) för de tärningar du vill kasta om separat med mellanslag. Exempel: Du vill kasta om första och andra tärningen, skriv: 0 4. För att spara alla tärningar, tryck Enter.")
            input_str = input("Dina val:").strip()

            if not input_str:
                return [] # om spelaren vill stanna och spara så är strängen tom
            valda_index = []
            delar = input_str.split()

            for del_str in delar:
                idx = int(del_str) # detta konverterar till heltal och kastar ValueError vid bokstäver.

                # ser till att indexet är i det korrekta intervallet
                if idx < 0 or idx > 4:
                    print("Ogiltigt index. Index är giltiga för mellan 0 och 4. Vänligen försök igen.")
                    break
                # ser till att spelaren inte kan ange samma index flera gånger
                if idx in valda_index:
                    print("Upprepat index klassas som ogiltigt index. Index är gitliga för mellan 0 och 4. Vänligen försök igen.")
                    break
                valda_index.append(idx)
            else:
                # om for-loopen kördes utan att bli avbruten av ett fel så körs 'else'
                return valda_index
        except ValueError:
            print("Endast siffror separerat med mellanslag är godkänt. Vänligen försök igen.")



## IDENTIFIERING
def analysera_hand(tarningar):
    """
    analyserar tärningarna efter kombinationer i en prioritetsordning.
    Sedan returnerar kombinationens namn och poängen.
    """
    # Sorterar tärnigarna i storleksordning vilket gör det lättare att identifiera en liten stege eller stor stege.
    sorterade = sorted(tarningar)
    # Gör en lista som räknar hur många gånger varje värde(1-6) förekommer
    frekvenser = [tarningar.count(i) for i in range(1, 7)]

# 1. Yatzy(5 lika tärningar)
    if 5 in frekvenser:
        return "Yatzy!", 50

# 2. Kåk(3 lika + 2 lika av en annan siffra/ett annat värde)
    if 3 in frekvenser and 2 in frekvenser:
        return "Kåk", sum(tarningar)

# 3. Stor stege(endast 2,3,4,5,6)
    if sorterade == [2, 3, 4, 5, 6]:
        return "Stor stege", 20

# 4. Liten stege(endast 1,2,3,4,5)
    if sorterade == [1, 2, 3, 4, 5]:
        return "Liten stege", 15

# 5. Fyrtal(4 lika tärningar)
    if 4 in frekvenser:
        return "Fyrtal", sum(tarningar)

# 6. Tretal(3 lika tärningar)
    if 3 in frekvenser:
        return "Tretal", sum(tarningar)

 # 7. Två Par(två olika par i samma hand)   
    if frekvenser.count(2) == 2:
        return "Två Par", sum(tarningar)
    
 # 8. Ett Par(två lika tärningar)   
    if 2 in frekvenser:
        return "Ett Par", sum(tarningar)

 # 9. Ingen kombination hittas då så faller tärningarnas summa tillbaka
    return "Ingen Kombination (Summa)", sum(tarningar)

## SPELRUNDA
def spela_runda():
    """
    Slår 5 tärningar, spelaren får två omkastningar med validering om den vill,
    sen presenteras slutresultatet av poängen för en enskild runda.
    """
    # här slumpas 5 tärningar för det första kastet
    tarningar = [random.randint(1, 6) for _ in range(5)]
    print("\n--- Ditt första kast ---")
    print("Tärningar:", tarningar)
    print("Index:     [0, 1, 2, 3, 4]")

    # här får spelaren max 2 chanser till omkast för de tärningar/index den väljer.
    for kast in range(2):
        print(f"\n--- Chans till omkastning {kast + 1}/2 ---")
        val = input("Vill du kasta om några tärningar? (ja/nej): ").strip().lower()

        if val == 'ja':
            # använder valideringsfunktionen för att få giltiga index utan att krascha.
            index_attkasta = validerahamta_index()

            # det avbryts och en tom lista returneras om spelaren tryckt Enter direkt.
            if not index_attkasta:
                print("Du har valt att inte kasta om några tärningar.")
                break

            # indexen får nya slumpade värden och visas i tärningslistan
            for idx in index_attkasta:
                tarningar[idx] = random.randint(1, 6)

            print("\nDina tärningar efter omkastning är följande:")
            print("Tärningar:", tarningar)
            print("Index:     [0, 1, 2, 3, 4]")
        else:
            print("Du har valt att stanna.")
            break


# Visar rundans slutresultat
    print("\n--- Rundan är klar! ---")
    print("Slutgiltig hand:", tarningar)

    # frekvenskartan visas efter det sista kastet
    frekvenskarta(tarningar)

    # analyserar tärningarna och räknar ut poängen
    resultat_namn, poang = analysera_hand(tarningar)
    print(f"\nResultat: {resultat_namn}!")
    print(f"Poäng denna runda: {poang} p")

    return poang


## MENY OCH POÄNGSYSTEM
def main():
    """
    Huvudloopen kör spelets meny, håller koll på totalpoäng och hur många rundor som spelats över tid.
    """
    total_poang = 0
    rundor_spelade = 0

    while True:
        print("\n================ YATZY MENY ================")
        print(f"Spelade rundor: {rundor_spelade}  -  Total poäng: {total_poang} p")
        print("--------------------------------------------")
        print("1. Spela en ny runda")
        print("2. Avsluta och nollställ (Nytt Spel)")
        print("3. Stäng av programmet")
        print("============================================")

        val = input("Välj ett alternativ (1-3): ").strip()
        # spelaren får välja vad den vill göra näst
        if val == '1':
            # val 1 ger en möjlighet för en ny runda, annars kan spelaren trycka Enter för att komma tillbaka till menyn.
            rundor_spelade += 1
            runda_poang = spela_runda()
            total_poang += runda_poang
            input("\nTryck Enter för att återvända till menyn...")

        elif val == '2':
            # om spelaren väljer val 2 så avslutas spelet och poängen nollställs/återgår till 0. Därefter startas ett nytt spel.
            print(f"\nDu avslutade spelet med {total_poang} poäng efter {rundor_spelade} rundor.")
            print("Startar ett nytt spel...")
            total_poang = 0
            rundor_spelade = 0
            input("\nTryck Enter för att fortsätta...")

        elif val == '3':
            # om spelaren väljer val 3 så kommer programmet stängas av och läsa den totala poängen.
            print(f"\nTack för att du spelade! Din slutgiltiga poäng blev: {total_poang} p.")
            break
        else:
            # om spelaren råkat skriva en bosktav eller något som inte är val 1, 2 eller 3 så kommer 'else' köras.
            print("Ogiltigt val. Val är giltiga för 1, 2 eller 3. Vänligen försök igen.")

if __name__ == "__main__":
    main()

