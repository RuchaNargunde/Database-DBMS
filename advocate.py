from tkinter import * 
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from functools import partial 

import pymysql

host_db="localhost"
user_db="root"
password_db="root"
db_name="sqlproject"

font14 = "-family {Segoe UI} -size 15 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
font16 = "-family {Swis721 BlkCn BT} -size 40 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
font9 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

db = pymysql.connect(host=host_db,user=user_db,password=password_db,database=db_name)

global advocate_id
advocate_id = 'A000001'     # user_id value to be imported and assigned to advocate_id

# 1. Show New Applications Functions

def accept_reject(value):
    case_id = Id1.get()
    if(case_id==""):
        messagebox.showwarning("Error","Enter Case Id")

    else:
        Id1.set("")
        db1 = pymysql.connect(host=host_db,user=user_db,password=password_db,database=db_name)
        cursor = db1.cursor()
        sql = "UPDATE cases set status=%s where case_id=%s"
        val = (value,case_id)
        cursor.execute(sql,val)
        db1.commit()
        messagebox.showinfo("Status","Case Accepted")
        db1.close()

def click_show_new_cases():
        global screen1
        screen1=Toplevel(root)
        screen1.title("Case Applications")
        screen1.geometry('900x600')

        message = Message(screen1,text="Case Applications",pady=10,width=500,font=font14)
        message.pack()

        CaseView = ttk.Treeview(screen1)
        CaseView["columns"] = ("case_name","case_details","client_name","case_type")
        CaseView.column("#0",width=40,minwidth=15)
        CaseView.column("case_name",width=135,minwidth=135)
        CaseView.column("case_details",width=325,minwidth=300)
        CaseView.column("client_name",width=150,minwidth=100)
        CaseView.column("case_type",width=150,minwidth=100)
        
        CaseView.heading("#0",text="Case ID",anchor=W)
        CaseView.heading("case_name",text="Case Name",anchor=W)
        CaseView.heading("case_details",text="Case Details",anchor=W)
        CaseView.heading("client_name",text="Client Name",anchor=W)
        CaseView.heading("case_type",text="Case Type",anchor=W)
               

        db = pymysql.connect(host=host_db,user=user_db,password=password_db,database=db_name)
        cursor = db.cursor()
        sqlQuery = "CREATE or REPLACE view names as select cases.case_name,cases.case_details,users.user_name,cases.case_type,clients.user_id,cases.case_id from ((cases INNER JOIN clients ON cases.case_id=clients.case_id) INNER JOIN users ON clients.user_id=users.user_id) where cases.status='PENDING' and cases.user_id=%s;"        
        cursor.execute(sqlQuery, advocate_id)
        sqlQuery1 = "SELECT * from names"
        cursor.execute(sqlQuery1)
        rows = cursor.fetchall()

        
        for i,row in enumerate(rows):            
            caseName = row[0]
            caseDetails = row[1]
            userName = row[2]
            caseType = row[3]
            userId = row[4]
            caseId = row[5]
            
            CaseView.insert("",i+1,text=caseId,values=(caseName,caseDetails,userName,caseType))
        
        CaseView.pack(side=TOP,fill=X)    

        db.close()

        global Id1
        Id1 = StringVar()
        Label(screen1,text="Enter Case ID: ",font=font9).pack(side=LEFT,padx=20)
        Entry(screen1,font=font9,textvariable=Id1,width=10).pack(side=LEFT,padx=20)
        AcceptButton = tk.Button(screen1,text="Accept",width=15,command=partial(accept_reject,"ACCEPTED"))
        RejectButton = tk.Button(screen1,text="Reject",width=15,command=partial(accept_reject,"REJECTED"))
        AcceptButton.pack(side=LEFT,padx=20)
        RejectButton.pack(side=LEFT,padx=20)

# 2. Show Current Cases Functions

def updateQuery():
    case_id = Id.get()
    if(E1.get()=="" or v2.get()=="" or v3.get()==""):
        messagebox.showwarning("Error","Enter All the Details!!!!!!")

    else:
        db1 = pymysql.connect(host=host_db,user=user_db,password=password_db,database=db_name)
        cursor = db1.cursor()
        sqlQuery = """UPDATE cases set case_details=%s,next_hearing_date=(STR_TO_DATE(%s, '%%d/%%m/%%Y')),pre_hearing_date=(STR_TO_DATE(%s, '%%d/%%m/%%Y')) where case_id=%s"""
        val = (E1.get(),v2.get(),v3.get(),case_id)
        print("In update Query")
        cursor.execute(sqlQuery,val)
        db1.commit()
        messagebox.showinfo("Status","Case Details Updated")
        db1.close()
        screen3.destroy()

def edit(case_name,case_details,case_type,next_hearing_date,pre_hearing_date):
    global screen3
    global E1,v2,v3
    case_id = Id.get()
    if(case_id==""):
        messagebox.showwarning("Error","Enter Case Id")

    else:
        screen3=Toplevel(screen2)
        screen3.title("Update Case Details")
        screen3.geometry('500x350')
        message = Message(screen3,text="Update Case Details",pady=10,width=400,font=font14)
        message.grid(row=0)

        list1 = ["Case Name:","Case Type:"]
        list2 = [case_name,case_type]
        nrow=1
        for i in range(len(list1)):
            Label(screen3, text=list1[i],font=font9,fg='gray50',pady=5).grid(row=nrow, column=0, sticky=W)
            Label(screen3,text=list2[i],font=font9,pady=5).grid(row=nrow,column=1,sticky=W,columnspan=4) 
            nrow += 1

        list3 = ["Case Details: ","Next Hearing Date: ","Previous Hearing Date: "]

        for i in range(len(list3)):
            Label(screen3, text=list3[i],font=font9,fg='gray50',pady=5).grid(row=nrow, column=0, sticky=W)
            nrow += 1

        v2 = StringVar()
        v3 = StringVar()
        E1 = Entry(screen3,width=40)
        E1.grid(row=3,column=1,columnspan=4)
        E1.insert(0,case_details)
        E2 = Entry(screen3,font=font9,textvariable=v2).grid(row=4,column=1,columnspan=4,sticky=W)
        E3 = Entry(screen3,font=font9,textvariable=v3).grid(row=5,column=1,columnspan=4,sticky=W)

        Button(screen3,text="Update",command=updateQuery).grid(row=6,rowspan=3,sticky=W+E+N+S,pady=20)

def click_show_cases():
        global screen2
        screen2 = Toplevel(root)
        screen2.title("Current Cases")
        screen2.geometry('900x600')

        message = Message(screen2,text="Current Cases",pady=10,width=500,font=font14)
        message.pack()

        CaseView2 = ttk.Treeview(screen2)
        CaseView2["columns"] = ("case_name","case_details","case_type","next_hearing_date","pre_hearing_date")
        CaseView2.column("#0",width=40,minwidth=15)
        CaseView2.column("case_name",width=135)
        CaseView2.column("case_details",width=325,minwidth=300)
        CaseView2.column("case_type",width=100,minwidth=100)
        CaseView2.column("next_hearing_date",width=100,minwidth=100)
        CaseView2.column("pre_hearing_date",width=100,minwidth=100)

        CaseView2.heading("#0",text="Case Id",anchor=W)
        CaseView2.heading("case_name",text="Case Name",anchor=W)
        CaseView2.heading("case_details",text="Case Details",anchor=W)
        CaseView2.heading("case_type",text="Case Type",anchor=W)
        CaseView2.heading("next_hearing_date",text="Next Hearing",anchor=W)
        CaseView2.heading("pre_hearing_date",text="Previous Hearing",anchor=W)
        CaseView2.pack(side=TOP,fill=X)
       
        global Id
        db = pymysql.connect(host=host_db,user=user_db,password=password_db,database=db_name)
        cursor = db.cursor()
        sqlQuery = "SELECT case_id,case_name,case_details,case_type,next_hearing_date,pre_hearing_date from cases where status='ACCEPTED'"
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        for i,row in enumerate(rows):
            caseId = row[0]
            caseName = row[1]
            caseDetails = row[2]
            caseType = row[3]
            nextHearing = row[4]
            preHearing = row[5]
            print(row)
            CaseView2.insert("", i+1, text=caseId, values=(caseName,caseDetails,caseType,nextHearing,preHearing))

        Id = StringVar()
        Label(screen2,text="Enter Case ID: ",font=font9).pack(side=LEFT,padx=20)
        Entry(screen2,font=font9,textvariable=Id,width=10).pack(side=LEFT,padx=20)
        Button(screen2,text="Edit",width=10,command=partial(edit,caseName,caseDetails,caseType,nextHearing,preHearing)).pack(side=LEFT,padx=20)
        

# Main Advicate Screen
class Advocate:
    def __init__(self):
        
        global root
        root = Tk()
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#ffffff' # X11 color: 'white'
        _ana1color = '#ffffff' # X11 color: 'white'
        _ana2color = '#ffffff' # X11 color: 'white'
        
        root.geometry("963x749+540+110")
        root.title("Advocate")
        root.configure(background="#d9d9d9")
        root.configure(highlightbackground="#d9d9d9")
        root.configure(highlightcolor="black")

        self.Frame1 = Frame(root)
        self.Frame1.place(relx=0.02, rely=0.03, relheight=0.94, relwidth=0.96)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=925)

        self.Message = Message(self.Frame1)
        self.Message.place(relx=0.09, rely=0.01, relheight=0.15, relwidth=0.86)
        self.Message.configure(background="#d9d9d9")
        self.Message.configure(font=font16)
        self.Message.configure(foreground="#000000")
        self.Message.configure(highlightbackground="#d9d9d9")
        self.Message.configure(highlightcolor="black")
        self.Message.configure(text='''WELCOME''')
        self.Message.configure(width=791)

        self.Button1 = Button(self.Frame1)
        self.Button1.place(relx=0.18, rely=0.17, height=103, width=566)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#bfbfbf")
        self.Button1.configure(font=font14)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady=10)
        self.Button1.configure(text='''1.SHOW CASE APPLICATIONS''')
        self.Button1.configure(width=566)
        self.Button1.configure(command=click_show_new_cases)


        self.Button2 = Button(self.Frame1)
        self.Button2.place(relx=0.18, rely=0.33, height=93, width=566)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#bfbfbf")
        self.Button2.configure(font=font14)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady=10)
        self.Button2.configure(text='''2.CURRENT CASES''')
        self.Button2.configure(width=566)
        self.Button2.configure(command=click_show_cases)

        self.Button3 = Button(self.Frame1)
        self.Button3.place(relx=0.18, rely=0.47, height=93, width=566)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(disabledforeground="#bfbfbf")
        self.Button3.configure(font=font14)
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="10")
        self.Button3.configure(text='''3.LOG OUT''')
        self.Button3.configure(width=566)
        # self.Button3.configure(command=click_logout)   return to main screen
        root.mainloop()

if __name__ == '__main__':
    GUUEST=Advocate()

