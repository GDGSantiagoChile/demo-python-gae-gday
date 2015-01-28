# encoding:utf-8
#!/usr/bin/env python

# imports básicos
import os
import webapp2
import jinja2


# import del modulo creado con el datastore
from modelos import RegistroContacto


# imports de modulos necesarios para usar oauth2
from oauth2client.appengine import OAuth2Decorator
from apiclient.discovery import build
import httplib2


# Crear una variable estática del entorno de nuestros templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.abspath('templates')),
    autoescape=True,
    extensions=['jinja2.ext.autoescape']
)


# creación del objeto decorator
decorator = OAuth2Decorator(
    client_id='1012452221438-9tpqm4tcg27262o0vmi5gbq88a8q35em.apps.googleusercontent.com',
    client_secret='iVPiX1TbbmVHaRVd8OX_vpMP',
    scope='https://www.googleapis.com/auth/userinfo.profile ' +
    'https://www.googleapis.com/auth/userinfo.email ',
)

# construcción del servicio de userinfo
http = httplib2.Http()
userinfo_service = build('oauth2', 'v2', http=http)


# Una clase controladora de peticiones HTTP (get, post, put, delete)
class ControladorInicio(webapp2.RequestHandler):
    
    @decorator.oauth_aware
    def get(self):
        
        # validar si el usuario Google esta o no autentificado
        if not decorator.has_credentials():
        	# creamos un objeto con parámetro para injectarlo en el template
            variables = {
                'url': decorator.authorize_url(),
                'has_credentials': decorator.has_credentials()
            }
            
            # declaración y obtención de un template
            template = JINJA_ENVIRONMENT.get_template('login.html')

            # renderizar el template con las variables injectadas
            self.response.write(template.render(variables))
        else:
            http = decorator.http()
            data = userinfo_service.userinfo().get().execute(http=http)
            variables = {'data': data,}
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(variables))


class ControladorRegistros(webapp2.RequestHandler):
    
    @decorator.oauth_required
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('form_registro.html')
        self.response.write(template.render())
    
    def post(self):

    	# recibir parametro por POST
    	nombre = self.request.get('nombre')
    	email = self.request.get('email')
    	comentario = self.request.get('comentario')

    	# crear instancia del objeto de RegistroContacto
    	registro = RegistroContacto()
    	registro.nombre = nombre
    	registro.email = email
    	registro.comentario = comentario

		# metodo de guardar objeto en el DataStore
    	registro.put()

    	# forma de redirigir a una url en webapp2
        self.redirect('/')


class ControladorListadoRegistros(webapp2.RequestHandler):
    
    @decorator.oauth_required
    def get(self):

    	registro = RegistroContacto()
    	registros = registro.listar_registros()
    	variables = {
    		'registros': registros,
    	}
        template = JINJA_ENVIRONMENT.get_template('listar_registros.html')
        self.response.write(template.render(variables))


# Manejo de url de nuestra aplicación
app = webapp2.WSGIApplication([
    ('/', ControladorInicio),
    ('/registro', ControladorRegistros),
    ('/listado', ControladorListadoRegistros),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
