from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from database import cursor

Builder.load_file('showresults.kv') # Carrega o arquivo login.kv

class AnswerInput(Screen):
	pass

class MainApp(App):

	global result

	cursor.execute("SELECT id, nome, cargo, email, cpf FROM users ORDER BY id ASC LIMIT 1")
	result = cursor.fetchone()
	print(result)
	nome = "Nome: " + result[1]
	cargo = "Cargo: " + result[2]
	email = "Email: " + result[3]
	cpf = "CPF: " + result[4]
	source_ = 'pessoas/pessoa.'+str(result[0])+'.1.jpg'

	def build(self):

		return AnswerInput()

if __name__ == '__main__':
	MainApp().run()
