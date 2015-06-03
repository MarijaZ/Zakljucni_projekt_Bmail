#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo
from google.appengine.api import users
from google.appengine.api import urlfetch
import json

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')

            params = {"logiran": logiran, "logout_url": logout_url, "users": user}

        else:
            logiran = False
            login_url = users.create_login_url("/")

            params = {"logiran": logiran, "user": user, "login_url": login_url}
        self.render_template("hello.html", params)


class PosljiSporociloHandler(BaseHandler):

    def get(self):
        self.render_template("novo_sporocilo.html")

    def post(self):
        tekst = self.request.get("sporocilo")
        prejemnik1 = self.request.get("prejemnik")
        sporocilo = Sporocilo(vnos=tekst, prejemnik=prejemnik1)  #prejemnik je iz models
        sporocilo.put()

        params = {"sporocilo": sporocilo}
        self.redirect_to("main")



class PoslanoHandler(BaseHandler):

    def get(self):
        uporabnik = str(users.get_current_user())
        sporocilo = Sporocilo.query(Sporocilo.from_user)
        params = {"sporocilo": sporocilo}

        self.render_template("poslano.html", params)


class PrejetoSporociloHandler(BaseHandler):

    def get(self):
        pass


class VremeHandler(BaseHandler):

    def get(self):
        #koda
        url = "http://api.openweathermap.org/data/2.5/weather?q=London,uk&units=metric"
        rezultat = urlfetch.fetch(url).content
        podatki = json.loads(rezultat)

        params = {"podatki": podatki}

        self.render_template("vreme.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main"),
    webapp2.Route('/novo_sporocilo', PosljiSporociloHandler),
    webapp2.Route('/prejeta_sporocila', PrejetoSporociloHandler),
    webapp2.Route('/poslano/<sporocilo_id:\d+>/', PoslanoHandler),
    webapp2.Route('/vreme', VremeHandler),
], debug=True)# Zakljucni_projekt_Bmail
