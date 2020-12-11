from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
import sqlite3
from database import connection, cursor
global connection, cursor
cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
resultado = cursor.fetchall()
print(resultado)
class Login(Screen):
	def do_login(self, loginText, passwordText):
		app = App.get_running_app()

		app.username = loginText
		app.password = passwordText

		app.config.read(app.get_application_config())
		app.config.write()

		self.txt_login = ''
		self.txt_cpf = ''
		self.txt_cargo = ''
		self.txt_email = ''

	def register_data(self):
		self.txt_login = self.ids.login.text
		self.txt_cpf = self.ids.cpf.text
		self.txt_cargo = self.ids.identificador.text
		self.txt_email = self.ids.email.text
	def eigen(self):
		os.system('py eigen.py')
	def register_foto(self):
		os.system('py detection.py')
		
	def insert_values_in_dabatase(self):


		self.register_data()
		print(self.txt_login)
		print(self.txt_cpf)
		print(self.txt_cargo)
		print(self.txt_email)

		try:
			cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
			resultado = cursor.fetchall()
			ids = []
			for x in resultado:
				ids.append(str(x).strip('()[].,'))
			ide = ids[0]
			print(resultado)
			cursor.execute(
				"""
				UPDATE users
				SET nome = ?, cargo = ?, email = ?, cpf = ?
				WHERE id = ? """,(str(self.txt_login), str(self.txt_cargo), str(self.txt_email), str(self.txt_cpf),int(ide)))
		except ValueError:
			self.ids.login.text = 'Os campos não podem ser vazios.' # Caso ele aperte o botão e não tenha escrito nada.
		except:
			self.ids.login.text = 'Dados Repetidos.'
		else:
			connection.commit()
			#connection.close() Se fechar, ele só vai aceitar 1 usuário e vai dar erro.
			self.clean_input_values()
			self.ids.login.text = str(self.txt_login) # Coloca o último valor salvo dentro do campo login

			
			
	def clean_input_values(self):

		""" Faz a limpeza dos inputs """

		
		self.ids.login.text = ''
		self.ids.identificador.text = ''
		self.ids.email.text = ''
		self.ids.cpf.text = ''	

class LoginApp(App):
	username = StringProperty(None)
	password = StringProperty(None)

	def build(self):
		manager = ScreenManager()

		manager.add_widget(Login(name='login'))
		

		return manager

	def get_application_config(self):
		if(not self.username):
			return super(LoginApp, self).get_application_config()

		conf_directory = self.user_data_dir + '/' + self.username

		if(not os.path.exists(conf_directory)):
			os.makedirs(conf_directory)

		return super(LoginApp, self).get_application_config(
			'%s/config.cfg' % (conf_directory)
		)

if __name__ == '__main__':
	LoginApp().run()
