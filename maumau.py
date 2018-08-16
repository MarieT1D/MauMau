"""
Kartendarstellung

        Eichel  Grass   Herz    Schelle
7       10      20      30      40
8       11      21      31      41
9       12      22      32      42
10      13      23      33      43
unter   14      24      34      44
ober    15      25      35      45
koenig  16      26      36      46
sau     17      27      37      47

"""
import random
#Mgliche Farben/Werte
farbe=("Eichel", "Gras", "Herz", "Schelle")
wert=("7","8","9","10","Unter","Ober","Koenig","Sau")

#Darstellung im Bot
pos_kartenwert_id=[i for i in range(8)]
pos_kartenfarbe_id=[(j+1)*10 for j in range(4)]

karten_ids=[(i+j)for j in pos_kartenfarbe_id
        for  i in pos_kartenwert_id]

#Dictionary Karte und Kartenname
pos_kartenzeichen=dict(zip(pos_kartenwert_id,wert))
pos_kartenfarben=dict(zip(pos_kartenfarbe_id,farbe))
pos_kartennamen=dict(zip(karten_ids,[(j+"_"+i)for j in farbe 
                       for  i in wert]))

no_players = 4


#stellt die farbe einer Karte fest
#Trumpf 0,Eichel 1,Gras 2,Herz 3,Schelle 4
def get_farbe(karte):
    return pos_kartenfarben[(karte//10)*10]
    
def get_punkte(karte):
    return punkt_wert[karte%10]

def get_zeichen(karte):
    return pos_kartenzeichen[karte%10]
    

class Karte():
    def __init__(self,id):
        
        self.id = id
        self.farbe   = get_farbe(id)
        self.zeichen = get_zeichen(id) 
        if self.zeichen== "7":
                self.wert= "zwei_ziehen"
        elif self.zeichen=="8":
                self.wert= "aussetzen"
        self.name    = str(self.farbe)+'_'+str(self.zeichen)
        self.loc     = 'None'
    
class Game():
        players=4
        def __init__(self,players):
                assert no_players < 6
                self.kartensatz=[Karte(i) for i in karten_ids]
                random.shuffle(self.kartensatz)
               # self.players = no_players
                self.players = players
                self.player_cards = dict(zip([i.id for i in self.players],[]*no_players))


        def reset(self):
            random.shuffle(self.kartensatz)

            for i in self.kartensatz:
                i.loc = 'gespielt'

            for i in range(no_players):
                for j in range(7):
                    self.kartensatz[i*7+j].loc = self.players[i].id
                self.players[i].handout(self.kartensatz[i*7:(i+1)*7])


        def check_karten(self):
            player_ids = [i.id for i in self.players]
            self.player_cards = dict(zip(player_ids,[[]for i in range(len(player_ids))]))
            for i in self.kartensatz:
                if i.loc in player_ids:
                    self.player_cards[i.loc].append(i)


        def play(self):

            es_gibt_einen_gewinner = False
            gelegt = self.kartensatz[no_players*7:]

            counter = 0

            while not(es_gibt_einen_gewinner):

                for i in range(no_players):
                    answer = self.players[i].lege(gelegt[-no_players:])
                    if answer != 0:
                        print(answer.loc)
                        print(self.players[i].id)
                        assert answer.loc == self.players[i].id     #schaut ob er die Karte hat
                        assert answer.farbe == gelegt[-1].farbe or answer.zeichen == gelegt[-1].zeichen
                        answer.loc = 'gespielt'
                        gelegt.append(answer)
                    if answer == 0:
                        j = random.randint(0,len(gelegt)-no_players)
                        gelegt[j].loc = self.players[j].id
                        self.players[i].nehme(gelegt[j])
                        gelegt.pop(j)
                        answer = self.players[i].lege([gelegt[-1]])
                        if answer !=0:
                            answer.loc = 'gespielt'
                            gelegt.append(answer)

                    self.check_karten()
                    for j in self.players:
                        if len(self.player_cards[j.id]) == 0:
                            es_gibt_einen_gewinner = True
                            winner = j
                            print('Grandios, ' +str(j.name)+ ' ist toll')

                    counter += 1
                    if counter %100 == 0:
                        print('Sie hätte '+str(counter)+' Karten gespielt')
        
                    if es_gibt_einen_gewinner:
                        break


            """
            Regeln:
            Karte darf nur einmal gespielt werden
            Stapeln neu und gelegt
            Welche Karte darf ich spielen
            Wer keine Karten mehr, hat gewonnen
            Wenn man nicht legen kann, muss man Karte ziehen
            besondere Regeln (aussetzen)
            """



                             
class Player():
    x=iter(list(range(no_players)))
    def __init__(self, name):
                self.name=name
                self.id= next(self.x)

    def get_kartenname(self):
        a=[self.handout[i].name for i in range(len(self.handout))]
        return a

    def get_kartenid(self):
        a=[self.handout[i].id for i in range(len(self.handout))]
        return a



class Playerbot(Player):
    def __init__(self,name):
        Player.__init__(self,name)
    def handout(self,karten):
        self.karten = karten
        for i in self.karten:
            assert i.loc == self.id

    def lege(self,gelegt):
        k=gelegt[-1]
        f=0
        for i in range(len(self.karten)):                
            if k.zeichen==self.karten[i].zeichen:
                f=self.karten[i]
            elif k.farbe==self.karten[i].farbe: 
                f=self.karten[i]
        return f

    def nehme(self,a):
        self.karten.append(a)
        assert self.karten[-1].loc == self.id



player = [Playerbot(str(i)) for i in range(no_players)]
tgame = Game(player)
tgame.reset()
tgame.play()
