import random
from tkinter import *
from tkinter import messagebox 
import mysql.connector as mysql 
# Enter your db details to make this work!
host_db="localhost"
user_db="root"
password_db=""
db_name=""
con=mysql.connect(host=host_db,user=user_db,password=password_db,database=db_name,auth_plugin='mysql_native_password')
def register_user():
	role_info=role.get()
	if role_info.lower() == "advocate":
		user_id="A"+str(random.randint(100000,999999))
	else:
		user_id="C"+str(random.randint(100000,999999))
	email_info=email.get()
	password_info=password.get()
	username_info=username.get()
	number_info=number.get()
	address_info=address.get()
	if email_info=="" or password_info=="" or username_info=="" or number_info=="" or address_info=="":
		top = Tk()  
		top.geometry("100x100")      
		messagebox.showinfo("Warning","Please Enter all details!")  
		top.mainloop()  
	else:
		cur=con.cursor()
		sql1="INSERT INTO users VALUES(%s,%s,%s,%s,%s)"
		val=(user_id,username_info,number_info,email_info,address_info)
		cur.execute(sql1,val)
		con.commit()
		messagebox.showinfo("Status","Registered Successfully")
		con.close()

def register():
	screen1=Toplevel(screen)
	screen1.title("Register")
	screen1.geometry('300x250')

	global email
	global password
	global username
	global number
	global address
	global role
	email=StringVar()
	password=StringVar()
	username=StringVar()
	number=StringVar()
	address=StringVar()
	role=StringVar()
	Label(screen1,text="").pack()
	Label(screen1,text="Please Enter your details").pack()
	Label(screen1,text="").pack()
	Label(screen1,text="Email *").pack()
	Entry(screen1,textvariable=email).pack()
	Label(screen1,text="").pack()
	Label(screen1,text="Password *").pack()
	Entry(screen1,textvariable=password,show="*").pack()
	Label(screen1,text="").pack()
	Label(screen1,text="Username").pack()
	Entry(screen1,textvariable=username).pack()
	Label(screen1,text="").pack()
	Label(screen1,text="Contact number").pack()
	Entry(screen1,textvariable=number).pack()
	Label(screen1,text="").pack()
	Label(screen1,text="Address").pack()
	Entry(screen1,textvariable=address).pack()
	Label(screen1,text="").pack()
	Label(screen1,text="Role").pack()
	Entry(screen1,textvariable=role).pack()
	Label(screen1,text="").pack()
	Button(screen1,text="Register",width='10',height='2',command=register_user).pack()

def check_credentials(email_id,password):
	cur=con.cursor()
	sql2="SELECT email_address FROM users WHERE email_address=%s"
	val=(email_id,)
	cur.execute(sql2,val)
	credentials=cur.fetchone()
	print(credentials)
	if not credentials:
		return False
	else:
		return email_id==credentials[0]

def login_user():
	log_email_info=log_email.get()
	log_password_info=log_password.get()
	if check_credentials(log_email_info,log_password_info):
		screen3=Toplevel(screen)
		screen3.geometry('300x250')
		screen3.title('Dashboard')
		Label(screen3,text="You're Successfully Logged in!").pack()		
	else:
		messagebox.showwarning("Status","Incorrect Credentials!")

def login():
	global log_email
	global log_password
	log_email=StringVar()
	log_password=StringVar()
	screen2=Toplevel(screen)
	screen2.title("Login")
	screen2.geometry('300x250')
	Label(screen2,text="Enter your email").pack()
	Entry(screen2,textvariable=log_email).pack()
	Label(screen2,text="").pack()
	Label(screen2,text="Enter your password").pack()
	Entry(screen2,textvariable=log_password,show="*").pack()
	Label(screen2,text="").pack()
	Button(screen2,text="Login",width='10',height='2',command=login_user).pack()

def main_screen():
	global screen
	screen=Tk()
	screen.geometry('300x250')
	screen.title('Welcome')
	Label(text='Welcome',bg='grey',width='300',height='2',font=("Calibri",13)).pack()
	Label(text="").pack()
	Button(text="Login",width='30',height='2',command=login).pack()
	Label(text="").pack()
	Button(text="Register",width='30',height='2',command=register).pack()
	screen.mainloop()

main_screen()