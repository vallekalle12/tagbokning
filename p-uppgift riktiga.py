from datetime import datetime # importerar datetime för att ta reda på nutid
import os # importerar os för att nå mitt egna filsystem
def rad_kolumn(n): # skapar hela matrisen för självaste vagnen
    kolumn = (n-1) // 4 #heltalsdivisionen blir kolumnen platsen hamnar i
    ratt_index = (n-1) % 4 # modulo av platsnumret blir raden
    reverse = (kolumn % 2 == 1) #om kolumnen är udda går stiger den i värde från andra hållet nedåt till uppåt
    if reverse:
        rad = 3-ratt_index # gör det som reverse ska göra
    else:
        rad = ratt_index
    mittgang = rad in (1,2) # kollar om det är mittgång
    tyst = kolumn < 4 # kollar om det är tyst avdelning
    return rad, kolumn, mittgang, tyst


class Tåg:
    def __init__(self, datum, avgtid, stracka, tagnr): # alla instanser klassen tåg ska ha
        self.datum = datum
        self.avgtid = avgtid
        self.stracka = stracka
        self.tagnr = tagnr
        self.vagnar = list()
        for nummer in range(1,6):
            vagn = Vagn(nummer,self)
            self.vagnar.append(vagn)

        
    
    
    
class Vagn:
    def __init__(self, nummer, tag):
        self.nummer = nummer
        self.tag = tag
        self.platser = []
        for n in range(1,33): # gör en for-slinga som räknar alla platser i en vagn
            rad, kolumn, mittgang, tyst = rad_kolumn(n) # det här tar numret och sätter in det i en funktion och sedan spottar den ut platsens egenskaper
            plats = Plats(n, nummer, mittgang=mittgang, tyst=tyst)
            self.platser.append(plats) # alla platser egenskaper sparar i en lista av objekt där varje plats är ett objekt
        


    def boka(self, antal, tyst, namn):
        lediga_platser = list()
        bokade_platser = list()
        sekvens = list() # Sekvens för att se om två platser är bredvid varandra
        sekvenser = list()
        mojligtbokadeplatser = list()
        hittad = 3
        for platser in self.platser: # kör igenom alla platser i vagnen
            if platser.booked == False and platser.tyst == tyst: # filtrerar till bokade och villkoret från kunden
                lediga_platser.append(platser) # sätter in de lediga platser som finns med villkoret
        # för att se om det finns tillräckligt många i avdelningen
        if antal > len(lediga_platser): # om en person vill boka fler platser än vad som finns i avdelningen
            rest = antal-len(lediga_platser) # resten av platser om man bokar så många som möjligt i avdelningen
            return rest # boka returnar en int om detta är fallet
        # funktion som jämför lediga platser och dess sammanhang
        if antal == 1:
            bokade_platser = lediga_platser[:antal]
            hittad = 1
        else:
            for i in range(len(lediga_platser)-1): # kollar hur platser följer på varandra
                if lediga_platser[i].platsnummer +1 == lediga_platser[i+1].platsnummer:
                    if lediga_platser[i] not in sekvens:
                        sekvens.append(lediga_platser[i])
                    if lediga_platser[i+1] not in sekvens: # filtrerar bort dubbletter
                        sekvens.append(lediga_platser[i+1])
                else:
                    if len(sekvens) > 0:
                        sekvenser.append(sekvens)
                        sekvens = []
            if len(sekvens) > 0:
                sekvenser.append(sekvens)
        # letar igenom de sekvenser som skapats och försöker sätta in antalet bokningar där
        for plats in sekvenser:
            if len(plats) >= antal:
                hittad = 2
                mojligtbokadeplatser.extend(plats[:antal])
                break
        # Jämför om man hittad en sekvens som passar bokningen eller inte
        if hittad == 2:
            bokade_platser = mojligtbokadeplatser
        elif hittad == 3:
                print('\nDet finns tyvärr inte tillräckligt många sammanhängande platser för din bokning.\n\nÄr det OK om platserna är splittrade? Svara JA eller NEJ.')
                fragasplittring = fraga_ja_nej('Ditt svar: ')              
                if fragasplittring == True:
                    bokade_platser = lediga_platser[:antal]
                else:
                    print('Tryck på \'Y\' för att ändra på din bokning\nTryck på \'X\' för att avbryta bokningen och återgå till huvudmenyn.')
                    val = fraga_bokstav('Ditt svar: ', ('X', 'Y'))
                    if val == 'X':
                            return None
                    else:
                        return 'ÄNDRING'
                    
                    
                            
                
        for plats in bokade_platser: # kör en for slinga i bokade listan för att sätta in att dom är bokade
            plats.booked = True # sätter att platsen är bokad
            plats.owner = namn # sätta dit namnet
        return bokade_platser


    def avboka(self, platsnummer):
        for plats in self.platser: # tar sig in i platser
            if plats.platsnummer == platsnummer: # för att sen kolla det platsnumret som är parametern
                if plats.booked == False: # om då den redan inte är bokad returnar den None så att main kan förstå det
                    return None
                else:
                    plats.booked = False # annars ändrar man till False och tar bort owner
                    plats.owner = ''
                return plats
            



    
    def __str__(self):
        rutnat = list()
        for r in range(4):
            rad = [None]*8 # sätter upp ett rutnät 4X8
            rutnat.append(rad)
        for plats in self.platser:
            rad, kolumn = rad_kolumn(plats.platsnummer)[:2]
            rutnat[rad][kolumn] = plats # kopplar ihop varje plats med en viss rad och kolumn
        rader = list()
        for rad in rutnat:
            texter = list()
            for ruta in rad:
                if ruta.booked == True:
                    texter.append(('*' + str(ruta.platsnummer) + '*').rjust(4))
                else:
                    texter.append((str(ruta.platsnummer) + ' ').rjust(4))
            texter.insert(4, '|'.rjust(1))
            rader.append(' '.join(texter))
        rader.insert(2, str('TYST AVD').center(20) + '|')
        return '\n'.join(rader)

      
            
class Plats:
    def __init__(self, platsnummer, vagnnummer, mittgang=False, tyst=False, booked=False, owner=''):
        self.platsnummer = platsnummer
        self.vagnnummer = vagnnummer
        self.mittgang = mittgang
        self.booked = booked
        self.owner = owner # alla instanser för klasses plats
        self.tyst = tyst

    def gora_biljett(self, tag): # gör biljetten med hjälp av instanserna
        rader = list() # används senare i funktionen, för att illustrera biljetten
        bredd = 30 # här med
        if self.mittgang == True:
            mittgang = 'Mittgång' # kollar om det är mittgång
        else:
            mittgang = 'Fönsterplats'
        if self.tyst == True: # om det är tyst avdelning
            tyst = 'Tyst avdelning'
        else:
            tyst = 'Vanlig avdelning'
        texter = ['PLATSBILJETT']
        texter.append(tag.stracka + ' ' + tag.avgtid )
        texter.append('Vagn' + ' ' + str(self.vagnnummer))
        texter.append( 'Plats' + ' ' + str(self.platsnummer))
        texter.append(tyst)
        texter.append(str(''+mittgang).center(30)) # gör en lista med allt som ska stå på biljetten
        texter.append(''+self.owner)
        for text in texter:
            rader.append('|' + text.center(bredd) + '|') # för att få en ram runt biljetten
        return '\n'.join(rader)
        
    
def skapa_taglista():
    nutid = datetime.now() 
    taglista = list()
    format_monster = '%Y-%m-%d %H:%M'
    radstrang = list()
    with open('tagavgangar.txt', 'r', encoding='utf-8') as tagfilen: # öppnar filen med tågavgångar
        tagavgangar = tagfilen.readlines()# läser in hela filen och gör det till en lista där raderna är element
        for tag in tagavgangar: # kommer in i varje tåg
            if tag.strip() == '': # hoppar över varje tom rad
                continue
            resultat = tuple(tag.strip().split(';')) # Här gör jag varje tågobjekt till en tuple med sina attributer
            datum, avgtid, stracka, tagnr = resultat # här sätter jag vad varje har för variabel
            avgang = datetime.strptime(f'{datum} {avgtid}',format_monster) # jämför tiden vid tågens avgång
            if avgang < nutid: # om de redan avgått kastas de bara iväg
                if os.path.exists(f'{datum}_{avgtid.replace(':','')}_{tagnr}.txt'):
                    os.remove(f'{datum}_{avgtid.replace(':','')}_{tagnr}.txt') # om avgången är passerad tar vi bort dess fil
            else:    
                tag = Tåg( datum,avgtid, stracka, tagnr) # annars sparas först tågobjektet i variabeln
                taglista.append(tag) # sedan sätts variabeln i en lista
    with open('tagavgangar.txt', 'w', encoding='utf-8') as avgangsfil: # ska skriva de tågavgångar som inte gått än
        for tag in taglista: # kommer in i objekten återigen
            rad = f'{tag.datum};{tag.avgtid};{tag.stracka};{tag.tagnr}\n' # gör vad en rad i filen ska se ut som
            avgangsfil.write(rad) #för att sen skriva raden
        return taglista # här är det vi ska returna till menyn för att de ska få sin tåglista


def valj_tag(taglista): # gjord för att printa ut de möjliga tågen
    for i, tag in enumerate(taglista, start=1): # enumerate fungerar bra här för att få ett index när man printar så att man kan välja
        print(str(i) + '. '+ tag.datum + ' : ' + tag.avgtid + ' : ' + tag.stracka + ' : ' + tag.tagnr)
    while True: # felsäkrar så att man väljer en befintlig avgång
        try:
            valavtag = int(input('Skriv in numret för det tåg du vill välja: '))
            if valavtag <= len(taglista) and valavtag > 0:
                break
            print('Det tåget finns inte försök igen!')
        except ValueError:
            print('Fel inmatning, försök igen!')
    return taglista[valavtag-1] #taglistan har egentligen index 0 vid valet 1 därför -1
    
    
def valja_vagn(tag): # väljer vagn
     for i, vagn in enumerate(tag.vagnar, start=1): # enumerate fungerar bra här också när man vill ha vilket nummer vagnen har
        print('VAGN' + ' '+ str(i) + ':')
        print(vagn)
        print()
     valavvagn = fraga_nummer(f'Välj din vagn 1-{len(tag.vagnar)}: ', 1, len(tag.vagnar))
     return tag.vagnar[valavvagn-1] # samma tanke här som med taglistan



def spara_bokning_i_fil(tag): # nu vill vi spara i en fil
    filfortag = f'{tag.datum}_{tag.avgtid.replace(':','')}_{tag.tagnr}.txt' # vad filen ska heta
    with open(filfortag, 'w', encoding='utf-8') as filen: # skapar filen och skriver i den
        for vagn in tag.vagnar:
            for plats in vagn.platser:
                if plats.booked == True:
                    filen.write(f'{vagn.nummer};{plats.platsnummer}\n') # skriver in numret av vagnen samt vilket platsnummer
                
def las_in_bokningar(taglista): # funktionen är till för att läsa in bokade platser som är 
    for tag in taglista:
        filnamn = f'{tag.datum}_{tag.avgtid.replace(':','')}_{tag.tagnr}.txt'
        try:
            with open(filnamn, 'r', encoding='utf-8') as tagfilen:
                rader = tagfilen.readlines()
                for rad in rader:
                    bokningsuppgifter = rad.strip().split(';')
                    vagnnummer, platsnummer = bokningsuppgifter
                    bokad_vagn = tag.vagnar[int(vagnnummer)-1]
                    for plats in bokad_vagn.platser:
                        if plats.platsnummer == int(platsnummer):
                            plats.booked = True
        except FileNotFoundError:
            continue

def finns_bokningar(taglista):
    for tag in taglista:
        for vagn in tag.vagnar:
            for plats in vagn.platser:
                if plats.booked == True:
                    return True
    return False


def summabokade(vagn): # den här funktionen kollar hur många platser som är bokade i vagnen
    summabokade = 0
    for plats in vagn.platser:
        if plats.booked == True:
            summabokade += 1
    return int(summabokade)
def ledigt_i_vagn(vagn, tyst): # den här visar hur många lediga platser det finns i vagnen
    antal = 0
    for plats in vagn.platser:
        if plats.booked == False and plats.tyst == tyst:
            antal +=1
    return antal
def forsok_boka(vagn, antal, tyst, namn): # här är en felsäkring som kollar om antalet bokningar är möjliga i avdelningen
    if antal > ledigt_i_vagn(vagn, tyst):
        return None
    bokning = vagn.boka(antal, tyst, namn)
    if type(bokning) == list:
        return bokning
    return None
    
def lagra(lista_biljetter, nya_biljetter):
    lista_biljetter.extend(nya_biljetter)
    return lista_biljetter
def fraga_ja_nej(text): # felsäkring för ja och nej frågor
    while True:
        svar = str.upper(input(text)).strip()
        if svar == 'JA':
            return True
        elif svar == 'NEJ':
            return False
        print('Svara \'Ja\' eller \'Nej\'')

def fraga_bokstav(text, alternativ): # felsäkring för de frågor jag har bokstäver som svar till
    while True:
        svar = str.upper(input(text))
        if svar in alternativ:
            return svar
        print(f'Svara något av dessa \'{alternativ}\' tack!')
def fraga_nummer(text, lagst, hogst): # felsäkring för ed frågor om en siffra
    while True:
        try:
            antal = int(input(text))
        except ValueError:
            print('Fel inmatning, en siffra tack!')
            continue
        if lagst <= antal <= hogst:
                return antal
        print(f'Välj ett tal mellan {lagst} och {hogst}')
def angra(platser): # Den här funktionen tar bort bokade platser som avbryts och ångrar dom
    for plats in platser:
        plats.booked = False
        plats.owner = ''
def planera_vagn(vagn,tyst,kvar): #  funktionen planerar hur många platser som är kvar i en vagn
    plan = list()
    i_vald = min(ledigt_i_vagn(vagn,tyst), kvar) # letar efter det minsta värdet, om det är kvar eller vagnen
    if i_vald > 0:
        plan.append((vagn, i_vald, tyst))
        kvar -= i_vald
    i_andra = min(ledigt_i_vagn(vagn, not tyst), kvar)
    if i_andra > 0:
        if tyst:
            andra = 'vanlig avdelning'
        else:
            andra = 'tyst avdelning'
        plan_fraga = fraga_ja_nej(f'{i_andra} platser får plats i {andra} i vagn {vagn.nummer}. Går det bra? Svara \'Ja\' eller \'Nej\': ')
        if plan_fraga == True:
            plan.append((vagn, i_andra, not tyst))
            kvar -= i_andra
    return plan, kvar
    
    
        



def meny():
    print('Vad vill du göra?\n\n    * Boka, skriv \'B\', på samma rad följt av önskat antal biljetter.\n    * Avboka, skriv \'A\', på samma rad följ av ett platsnummer.')
    print('    * Skriva ut de senast bokade biljetterna, skriv \'S\'\n    * Avsluta, skriv \'Q\'\n\n')
    alternativ = ('B', 'S', 'A', 'Q')
    bokstavsval = fraga_bokstav('Ditt val: ', alternativ)
    return bokstavsval
    
def main():
    plats_per_vagn = 32 # totalt i en vagn
    taglista = skapa_taglista()
    if taglista == []: # om det inte finns några tåg
        print('Det finns tyvärr inga tåg att boka just nu :)')
        return
    lista_biljetter = list()
    las_in_bokningar(taglista)
    senaste_tag = None

    
    while True:
        val = meny() # gör en meny för programmet
        
        if val == 'B':
            tag = valj_tag(taglista) # val av tåg
            vagn = valja_vagn(tag) # val av vagn
            
            while True:
                lediga_platser_i_vagn = plats_per_vagn-summabokade(vagn) # kollar hur många lediga platser det finns i vagnen
                lediga_platser_i_tag = 0
                for v in tag.vagnar:
                    lediga_platser_i_tag += plats_per_vagn-summabokade(v) # kollar hur många platser det finns att boka i tåget
                if lediga_platser_i_tag == 0: # om det inte finns några platser
                    print('Tåget är tyvärr fullbokat :(')
                    break
                antal = fraga_nummer('Hur många platser vill du boka?: ', 1, lediga_platser_i_tag)
                tyst = fraga_ja_nej('Vill du ha tyst avdelning svara \'Ja\' eller \'Nej\' endast: ')
                namn = str(input('På vilket namn ska bokningen stå på? '))
                if antal <= lediga_platser_i_vagn: # om antalet är mindre än platser i vagnen
                    bokning = vagn.boka(antal, tyst, namn)

                    if type(bokning) != int and bokning != 'ÄNDRING' and bokning != None: # om boka inte returnar en integer och ändring och None
                        lista_biljetter = bokning # här sparas varje objekt som skapats i en lista med biljetter
                        senaste_tag = tag
                        spara_bokning_i_fil(tag)
                        break
                    elif bokning == None: # det här blir om svaret är att man vill avbryta sin bokning om splittrade platser
                        break
                    elif bokning == 'ÄNDRING': # här är istället om man vill ändra sin bokning
                        continue
                    else: # else satsen blir om bokning = int eller resten
                        print('\n\n')
                        print('du har bokat för många platser i avdelningen.')
                        print('Vill du boka resterande platser i den andra avdelningen')
                        felval = fraga_ja_nej('Skriv \'Ja\' eller \'Nej\': ')
                        if felval == True: # det här är koden jag använder för om det är okej med olika avdelninga
                            avdelningsbokningar = antal-bokning # räknar ut hur många som är kvar
                            if ledigt_i_vagn(vagn, not tyst) >= bokning: 
                                if avdelningsbokningar > 0:
                                    vanliga = forsok_boka(vagn, avdelningsbokningar, tyst, namn)
                                else:
                                    vanliga = []
                                restbokningar = forsok_boka(vagn, bokning, not tyst, namn)

                                if vanliga is not None and restbokningar is not None:
                                    lista_biljetter = vanliga + restbokningar
                                    senaste_tag = tag
                                    spara_bokning_i_fil(tag)
                                    break
                                
                                for lista in (vanliga, restbokningar):
                                    if lista:
                                        for plats in lista:
                                            plats.booked = False
                                            plats.owner = ''
                                print('Bokningen gick tyvärr inte igenom.')
                            else:
                                print('Den andra avdelningen har inte heller tillräckligt med plats')
                           
                        else:
                            valvill = fraga_bokstav('\nSkriv \'H\' om du vill tillbaka till menyn\nSkriv \'Ä\' om du vill ändra på din bokning: ', ('H', 'Ä'))
                            if valvill == 'H':
                                break
                            else:
                                continue
                else:
                    print('Det finns inte tillräckligt många platser i vagnen för din bokning,!')
                    plan, kvar = planera_vagn(vagn, tyst, antal)
                    print(f'{kvar} platser får inte plats i vagn {vagn.nummer}.')
                    valavfraga = fraga_ja_nej('Vill du boka resterande platser i en annan vagn? Svara \'Ja\' eller \'Nej\': ')
                    if valavfraga == True:
                        valda_vagnar = [vagn.nummer]
                        avbruten = False
                        while kvar > 0 and not avbruten:
                            print(f'Du har {kvar} platser kvar att placera. Välj en vagn till')
                            nyvagn = valja_vagn(tag)
                            if nyvagn.nummer in valda_vagnar:
                                print('Den vagnen har du redan valt!')
                            else:
                                nytyst = fraga_ja_nej('Vill du ha tyst avdelning i den vagnen?: ')
                                nyplan, kvar= planera_vagn(nyvagn, nytyst, kvar)
                                if nyplan == []:
                                    print('Det gick inte att boka något i den vagnen.')
                                else:
                                    plan += nyplan
                                    valda_vagnar.append(nyvagn.nummer)
                            if kvar > 0:
                                svarvaljavagn = fraga_ja_nej('Vill du fortsätta välja vagn? Svara \'Ja\' om du vill det. Svara \'Nej\' om du vill avbryta!')
                                if svarvaljavagn == False:
                                    avbruten = True
                        if avbruten:
                            print('Bokningen avbröts, inga platser bokades!')
                            break

                        biljetter = list()
                        lyckades = True
                        for delvagn, delantal, deltyst in plan: # Här bokas allt på riktigt
                            delbokning = forsok_boka(delvagn, delantal, deltyst, namn)
                            if delbokning == None: # kollar om delbokning returnar None
                                lyckades = False
                                break
                            biljetter += delbokning # om det returnar
                        if lyckades == True:
                            lista_biljetter = biljetter # här gör vi en lista med biljetter för att komma ihåg 
                            senaste_tag = tag
                            spara_bokning_i_fil(tag)
                            print('Du har nu bokat biljetter till din resa.')
                            break
                        angra(biljetter)
                        print('Bokningen gick tyvärr inte igenom, du skickas nu till huvudmenyn.')
                        break
                    else:
                        fraga = fraga_bokstav('Tryck på \'L\' om du vill avbryta bokningen eller \'G\' om du vill ändra bokningen: ',('L', 'G'))
                        if fraga == 'L':
                            break
                        elif fraga == 'G':
                            continue
                        
                        

        elif val == 'A': # om svaret är A
            tag = valj_tag(taglista)
            vagn = valja_vagn(tag)
            if summabokade(vagn) == 0: # felsäkring för att se om det ens finns några biljetter att avboka
                print('Ingen plats är bokad i den vagnen.')
            else:
                while True:
                        platsnummer = fraga_nummer('vilket plats vill du avboka?: ', 1, plats_per_vagn)
                        avbokad = vagn.avboka(platsnummer)
                        if avbokad is None: # en till felsäkring, se till att platsen faktiskt är bokad
                           print('Den platsen är inte bokad')
                           avbrytfraga = fraga_ja_nej('vill du försöka igen svara \'Ja\' eller \'Nej\'')
                           if avbrytfraga == False:
                               break
                        else:
                            if avbokad in lista_biljetter:
                                lista_biljetter.remove(avbokad)
                            spara_bokning_i_fil(tag) # sparar den nya avbokningen i filen för tåget
                            break
                
            
        elif val == 'S':
            if lista_biljetter == []:
                print('Gör en bokning först för att kunna skriva ut biljetter!\n')
                continue
            else:
                with open('utskriftbiljetter.txt', 'w', encoding='utf-8') as biljettfilen:
                    for plats in lista_biljetter:
                        biljetter = plats.gora_biljett(senaste_tag)
                        biljettfilen.write(biljetter + '\n\n\n\n')
            
        
        elif val == 'Q':
            if len(lista_biljetter) > 0: # om man bokat
                print('Tack för att du väljer Stålbröst Järnvägar :)')
            else: # om man inte har bokat
                print('Avslutar programmet..')
            break
        else:
            print('Skriv in ett alternativ tack!')
        
main()
