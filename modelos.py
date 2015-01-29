# encoding:utf-8
#!/usr/bin/env python

import datetime


# import a la modulo NDB (New DB)
from google.appengine.ext import ndb


class RegistroContacto(ndb.Model):

    nombre = ndb.StringProperty()
    email = ndb.StringProperty()
    comentario = ndb.TextProperty()
    fecha_registro = ndb.DateTimeProperty(auto_now_add=True)

    def listar_registros(self):
        return RegistroContacto.query().fetch()

    def buscar_registro(self, email):
        return RegistroContacto.query(RegistroContacto.email == email).get()
