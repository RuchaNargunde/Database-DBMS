from tkinter import *
import tkinter.ttk as tk
import pymysql

def search_by_name( search_by , tree):
	
	print(search_by)

	sql="select user_name,specialisation,total_cases,cases_won,win_percentage from advocate left join advocate_names on advocate.user_id=advocate_names.user_id where user_name like "+"\'"+search_by+"%\';"
	cur.execute(sql)
	output=cur.fetchall()
	print(output)

	tree.delete(*tree.get_children())

	tree.insert("",'end',values=("\n"))

	for i,x in enumerate(output):
		x=list(x)
		print(x)

		tree.insert("",i+1, text="\t"+x[0], values=("\t\t"+x[1],"\t\t"+str(x[2]),"\t\t"+str(x[3]),"\t\t"+str(x[4])))


def search_by_specialisation(search_by,tree):

	sql="select user_name,specialisation,total_cases,cases_won,win_percentage from advocate left join advocate_names on advocate.user_id=advocate_names.user_id where specialisation like "+"\'"+search_by+"%\';"
	cur.execute(sql)
	output=cur.fetchall()
	print(output)

	tree.delete(*tree.get_children())

	tree.insert("",'end',values=("\n"))

	for i,x in enumerate(output):
		x=list(x)
		print(x)

		tree.insert("",i+1, text="\t"+x[0], values=("\t\t"+x[1],"\t\t"+str(x[2]),"\t\t"+str(x[3]),"\t\t"+str(x[4])))



def search_lawyers():

	search_frame=Toplevel(root)
	search_frame.title("Search Lawyers")
	search_frame.geometry("1500x1000")

	search=Entry(search_frame,font=('Times','14'))
	search.place(relx=0.17,rely=.1,width=550,height=30)

	btn_search=Button(search_frame,text="Search By Name",font=('Times','13'),command=lambda:search_by_name(search.get(),tree)).place(relx=0.57,rely=.1)
	btn_search=Button(search_frame,text="Search By Specialisation",font=('Times','13'),command=lambda:search_by_specialisation(search.get(),tree)).place(relx=0.67,rely=.1)



	style=tk.Style()
	style.configure("mystyle.Treeview.Heading",font=('Times',15,'bold'),pady=40)
	style.configure("mystyle.Treeview", font=('Times',13))


	tree=tk.Treeview(search_frame,style="mystyle.Treeview")
	tree["columns"]=("one","two","three","four")
	tree.column("#0",width=250,minwidth=250)
	tree.column("one",width=250,minwidth=250)
	tree.column("two",width=250,minwidth=250)
	tree.column("three",width=250,minwidth=250)
	tree.column("four",width=250,minwidth=250)

	
	tree.heading("#0",text="Advocate Name")
	tree.heading("one", text="Total cases fought")
	tree.heading("two", text="Specialisation")
	tree.heading("three", text="Cases won")
	tree.heading("four", text="Win-Percentage")
	tree.insert("",'end',values=("\n"))



	sql= "create or replace view advocate_names as select user_id,user_name from users where user_id like 'A%';"
	cur.execute(sql)
	sql="select user_name,specialisation,total_cases,cases_won,win_percentage from advocate left join advocate_names on advocate.user_id=advocate_names.user_id;"
	cur.execute(sql)
	results=cur.fetchall()

	for i,x in enumerate(results):
		x=list(x)
		print(x)

		tree.insert("",i+1, text="\t"+x[0], values=("\t\t"+x[1],"\t\t"+str(x[2]),"\t\t"+str(x[3]),"\t\t"+str(x[4])))

	tree.place(relx=0.5,rely=0.35,anchor="center")


def register(id,case_Type,case_Name,case_Details,advocate_Name,register_frame):

	sql="insert into clients (user_id,payment_status) values ("+"\'"+id+"\'"+",\'"+"Not Yet Paid"+"\');"
	cur.execute(sql)
	db.commit()

	sql= "create or replace view advocate_names as select user_id,user_name from users where user_id like 'A%';"
	cur.execute(sql)

	sql="select user_id from advocate_names where user_name="+"\""+advocate_Name+"\";"
	cur.execute(sql)	
	advocate_id=cur.fetchall()
	print(advocate_id[0][0])

	sql="select case_id from clients where user_id="+"\""+id+"\";"
	cur.execute(sql);
	case_id=cur.fetchall()
	print(case_id)
	print(case_id[len(case_id)-1][0])

	sql= " insert into cases (user_id,case_id,case_name,case_details,case_type,status) values (" + "\"" + advocate_id[0][0] + "\",\"" + str(case_id[len(case_id)-1][0]) + "\",\"" + case_Name + "\",\"" + case_Details + "\",\"" + case_Type + "\"," + "\"Pending\"); " 
	cur.execute(sql)
	db.commit()

	register_frame.destroy()

def register_new_case(id):

	register_frame=Toplevel(root)
	register_frame.title("Register New Case")
	register_frame.geometry("1500x1000")

	title=Label(register_frame,text="Please fill the following details:",font=('Times','14','bold'))
	title.place(relx=.5,rely=.1,anchor="center")

	case_type=Label(register_frame,text='Specify the case type:',font=('Times','14')).place(relx=.3,rely=.2)
	caseType=Entry(register_frame,font=('Times','14'),borderwidth=1,relief='solid')
	caseType.place(relx=.43,rely=.2,width=455,height=30)

	case_name=Label(register_frame,text='Specify the case name:',font=('Times','14')).place(relx=.3,rely=.3)
	caseName=Entry(register_frame,font=('Times','14'),borderwidth=1,relief='solid')
	caseName.place(relx=.43,rely=.3,width=455,height=30)

	case_details=Label(register_frame,text='Mention the case details:',font=('Times','14')).place(relx=.3,rely=.4)
	caseDetails=Text(register_frame,width=50,height=10,bd=1,font=('Times','14'),relief='solid')
	caseDetails.place(relx=.43,rely=.4)

	advocate_name=Label(register_frame,text='Name of the advocate you wish to hire:',font=('Times','14')).place(relx=.3,rely=.7)
	advocateName=Entry(register_frame,font=('Times','14'),borderwidth=1,relief='solid')
	advocateName.place(relx=.5,rely=.7,width=350,height=30)

	btn_submit=Button(register_frame,text='Submit',font=('Times','14'),command=lambda:register(id,caseType.get(),caseName.get(),caseDetails.get("1.0","end-1c"),advocateName.get(),register_frame))
	btn_submit.place(relx=.5,rely=.8,anchor='center')



def notification(id):

	notification_frame=Toplevel(root)
	notification_frame.title("Notifications")
	notification_frame.geometry("1500x1000")

	sql= "create or replace view advocate_names as select user_id,user_name from users where user_id like 'A%';"
	cur.execute(sql)

	title=Label(notification_frame,text="Check your notifications below:",font=('Times','16','bold')).place(relx=.5,rely=.1,anchor="center")

	hearing_dates=Label(notification_frame,text="Check Upcoming hearing dates here:",font=('Times','14','bold')).place(relx=.15,rely=.2)

	sql="  select case_name,next_hearing_date from cases where next_hearing_date between curdate() and date_add(curdate(), interval 1 month); "
	cur.execute(sql)
	output=cur.fetchall()
	# print(output)

	y=.15
	index=1

	for x in output:
		string1=str(index)+"."+" Case Name:"+str(x[0])
		string2=" Next Hearing Date: "+str(x[1])
		y=y+.1
		index+=1
		l1=Label(notification_frame,text=string1,font=('Times','14')).place(relx=.15,rely=y)
		l2=Label(notification_frame,text=string2,font=('Times','14')).place(relx=.15,rely=y+.03)


	y=y+.1
	level=y;

	accepted_cases=Label(notification_frame,text="Find all the accepted cases below: ",font=('Times','14','bold')).place(relx=.15,rely=y)

	sql="select user_name,case_name from ( advocate_names right join cases on advocate_names.user_id=cases.user_id ) where status='accepted';"
	cur.execute(sql)
	output=cur.fetchall()

	y=y+.06
	index=1

	for x in output:
		string1=str(index)+"."+" Advocate Name:"+str(x[0])
		string2=" Case Name: "+str(x[1])
		index+=1
		l1=Label(notification_frame,text=string1,font=('Times','14')).place(relx=.15,rely=y)
		l2=Label(notification_frame,text=string2,font=('Times','14')).place(relx=.15,rely=y+.03)
		y=y+.1


	y=.2

	pending_cases=Label(notification_frame,text="Find all the pending cases below: ",font=('Times','14','bold')).place(relx=.55,rely=y)

	sql="select user_name,case_name from ( advocate_names right join cases on advocate_names.user_id=cases.user_id ) where status='pending';"
	cur.execute(sql)
	output=cur.fetchall()

	y=.15
	index=1

	for x in output:
		string1=str(index)+"."+" Advocate Name:"+str(x[0])
		string2=" Case Name: "+str(x[1])
		y=y+.1
		index+=1
		l1=Label(notification_frame,text=string1,font=('Times','14')).place(relx=.55,rely=y)
		l2=Label(notification_frame,text=string2,font=('Times','14')).place(relx=.55,rely=y+.03)

	y=level

	rejected_cases=Label(notification_frame,text="Find all the rejected cases below: ",font=('Times','14','bold')).place(relx=.55,rely=y)

	sql="select user_name,case_name from ( advocate_names right join cases on advocate_names.user_id=cases.user_id ) where status='rejected';"
	cur.execute(sql)
	output=cur.fetchall()

	y=y+.06
	index=1

	for x in output:
		string1=str(index)+"."+" Advocate Name:"+str(x[0])
		string2=" Case Name: "+str(x[1])
		index+=1
		l1=Label(notification_frame,text=string1,font=('Times','14')).place(relx=.55,rely=y)
		l2=Label(notification_frame,text=string2,font=('Times','14')).place(relx=.55,rely=y+.03)
		y=y+.1




db=pymysql.connect("localhost","root","rucha@123","dbms_final_2")

root=Tk()
root.geometry("1500x1000")

if(db):
    print("connection successful")
    welcome=Label(root,text="WELCOME",font=("Times","24","bold"))
    welcome.place(relx=.5, rely=.25,anchor="center")

    btn_notification=Button(text="NOTIFICATIONS",font=("Times",'14'),padx=40,command=lambda:notification('C0001'))
    btn_notification.place(relx=.5,rely=.35,anchor="center")

    btn_newCase=Button(text="REGISTER NEW CASE",font=("Times",'14'),padx=8,command=lambda:register_new_case('C0001'))
    btn_newCase.place(relx=.5,rely=.43,anchor="center")

    btn_search=Button(text="SEARCH LAWYERS",font=("Times",'14'),padx=20,command=search_lawyers)
    btn_search.place(relx=.5,rely=.51,anchor="center")

    btn_records=Button(text="MY CASE RECORDS",font=("Times",'14'),padx=20)
    btn_records.place(relx=.5,rely=.59,anchor="center")



else:
    print("connection failed")

cur=db.cursor()

root.mainloop()