from google.appengine.ext import ndb


class Sporocilo(ndb.Model):
    vnos = ndb.TextProperty()
    prejemnik = ndb.StringProperty()
    posiljatelj = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    izbrisano = ndb.BooleanProperty(default=False)  #ni izbrisano iz baze, le uporabnik tako vidi, da je

class Uporabnik(ndb.Model):
    ime_priimek = ndb.StringProperty()
    tekst = ndb.StringProperty()
    geslo = ndb.StringProperty()
    sifrirano_geslo = ndb.StringProperty()

# Zakljucni_projekt_Bmail
