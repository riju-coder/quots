from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager , Screen
import json,random
from datetime import datetime
from pathlib import Path
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import glob

Builder.load_file('design.kv')

class LoginScreen(Screen):
	def signup(self):
		self.manager.current = "signup_screen"
	def get_login(self,uname,pword):
		with open('users.json') as file:
			users = json.load(file)
		if uname == "" or pword == "" :
			anim = Animation(color = (0.6, 0.7, 0.1, 1))
			anim.start(self.ids.login_wrong)
			self.ids.login_wrong.text = "Enter a valid user name or password"
		elif uname in users and users[uname]["password"] == pword:
			self.manager.transition.direction = "left"
			self.manager.current = "login_screen_success"
		else :
			anim = Animation(color = (0.6, 0.7, 0.1, 1))
			anim.start(self.ids.login_wrong)
			self.ids.login_wrong.text = "Invalid user name or password !"
	def forgot(self):
		self.manager.current = "forgot_pas"

class SignupScreen(Screen):
	def add_user(self,uname,pword):
		with open('users.json') as file:
			users = json.load(file)
		if not uname in users:
			users[uname] = {"username":uname,"password":pword,
	            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
			with open('users.json','w') as file:
				json.dump(users,file)
			self.manager.transition.direction = "left"
			self.manager.current = "signup_screen_success"
		elif uname == "" or pword == "" :
			anim = Animation(color = (0.6, 0.7, 0.1, 1))
			anim.start(self.ids.sign_up_text)
			self.ids.sign_up_text.text = "Enter a valid user name or password"
		else:
		    anim = Animation(color = (0.6, 0.7, 0.1, 1))
		    anim.start(self.ids.sign_up_text)
		    self.ids.sign_up_text.text = "User alredy exists !"
	     

class SignupScreenSuccess(Screen):
	def go_back(self):
		self.manager.transition.direction = "right"
		self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
	def logout(self):
		self.manager.transition.direction = "right"
		self.manager.current = "login_screen"
		self.manager.transition.direction = "left"
		
	def get_quote(self,feel):
		feel = feel.lower()
		ava = glob.glob('texts/*txt')
		ava = [Path(filename).stem for filename in ava]
		if feel in ava:
			with open(f"texts/{feel}.txt") as file:
				quots = file.readlines()
			self.ids.quote.text = random.choice(quots)
		else:
			self.ids.quote.text = "Try another option"

class ForgotPassword(Screen):
	def signup(self):
		self.manager.current = 'signup_screen'

class RootWidget(ScreenManager):
    pass

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()