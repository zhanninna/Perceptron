import os
import math
from random import randint
#import wikipedia

alfa = 1 #stala uczenia


def normalizuj(vector):
    maks_v = max(vector)
    ind = vector.index(maks_v)
    vector2_normalizacja = len(vector) * [0]
    vector2_normalizacja[ind] = 1
    return vector2_normalizacja


def text_rozklad(tekst):
    tekst = tekst.lower()
    tekst = [znak for znak in tekst if znak.isalpha()]
    licznosc = 26 * [0]
    for znak in tekst:
        if ord(znak) - 97 >= 26:
            print(f"Nieporpawny znak {ord(znak)} {znak}")
        else:
            licznosc[ord(znak) - 97] += 1
    return [x / len(tekst) for x in licznosc]


class Jezyk:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        path = "dane/" + nazwa
        self.pliki = [path + "/" + file for file in os.listdir(path)]

    def __str__(self):
        return f"({self.nazwa} {self.pliki})"

    def __repr__(self):
        return self.__str__()

    def zaladuj(self):
        self.rozklady = []
        for i, nazwa_pliku in enumerate(self.pliki):
            with open(nazwa_pliku, "r", encoding="utf-8") as f:
                tekst = f.read().lower()
                self.rozklady.append(text_rozklad(tekst))


class Perceptron:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.T = randint(-5, 5)
        self.wagi = [randint(-5, 5) for x in range(26)]

    def __str__(self):
        return f"{self.nazwa} T: {self.T} Wagi: {self.wagi}"

    def unipolarny(self, wektor_wejsciowy):
        net = 0
        for i in range(26):
            net = net + self.wagi[i] * wektor_wejsciowy[i]
        # if net >= self.T:
        #     net = 1
        # else:
        #     net = 0
        return 1 / (1 + (math.e ** (-net)))

    def delta(self, vector2, y, d):
        self.T = self.T + (d - y) * alfa * (-1)

        for i in range(26):
            self.wagi[i] = self.wagi[i] + (d - y) * alfa * vector2[i]


def main():
    jezyki = os.listdir("dane")

    jez = []
    percept = []
    for nazwa_jezyka in jezyki:
        obj = Jezyk(nazwa_jezyka)
        obj.zaladuj()
        jez.append(obj)
        p = Perceptron(nazwa_jezyka)
        percept.append(p)

    for i in range(1000):
        for index_jezyka, jezyk in enumerate(jez):
            for rozklad in jezyk.rozklady:
                wynik = []
                for p in percept:
                    wynik.append(p.unipolarny(rozklad))
                wynik = normalizuj(wynik)
                oczekiwane = len(jez) * [0]
                oczekiwane[index_jezyka] = 1
                for y, d, p in zip(wynik, oczekiwane, percept):
                    if y != d:
                        p.delta(rozklad, y, d)


    plik = input("Podaj nazwe pliku: ")
    tekst = text_rozklad(open(plik, "r", encoding="utf-8").read())

    # wikipedia.set_lang("de")
    # page = wikipedia.random()
    # tekst = wikipedia.summary(page)
    # print(tekst)
    # tekst = text_rozklad(tekst)


    wyniki = []
    for p in percept:
        wyniki.append(p.unipolarny(tekst))
    wyniki = normalizuj(wyniki)

    for i in range(len(wyniki)):
        if wyniki[i] == 1:
            print(f"Jezyk to: {jezyki[i]}")

    print(jezyki)
    print(wyniki)


if __name__ == '__main__':
    main()



