import tkinter as tk
import sqlite3
from tkinter import ttk,messagebox

def update(rows):
    tree.delete(*tree.get_children())
    for  i in rows:
        tree.insert('','end',values=i)

def search():
    q2=q.get()
    query="SELECT customer_id,first_name,last_name,age FROM customers WHERE first_name LIKE '%"+q2+"%'OR last_name LIKE '%"+q2+"%'"
    cursor.execute(query)
    rows=cursor.fetchall()
    update(rows)

def clear():
    cursor.execute("SELECT customer_id,first_name,last_name,age FROM customers")
    rows=cursor.fetchall()
    update(rows)

def getrow(event):
    rowid=tree.identify_row(event.y)
    item=tree.item(tree.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])

def delete_customer():
    cust_id=t1.get()
    if messagebox.askyesno('Confirm Delete','Are you sure you want to remove customer?'):
        query="DELETE FROM customers WHERE customer_id LIKE'%"+cust_id+"%'"
        cursor.execute(query)
        conn.commit()
        clear()
    else:
        return True
def add_new():
    cust_id=t1.get()
    fname=t2.get()
    lname=t3.get()
    age=t4.get()
    query="INSERT INTO customers (customer_id,first_name,last_name,age)VALUES(?,?,?,?)"
    cursor.execute(query,(cust_id,fname,lname,age))
    conn.commit()
    clear()
def update_customer():
    cust_id=t1.get()
    fname=t2.get()
    lname=t3.get()
    age=t4.get()
    if messagebox.askyesno('confirm','Are you sure you want to update customer?'):
        query="UPDATE customers SET first_name=?,last_name=?,age=? WHERE customer_id=?"
        cursor.execute(query,(fname,lname,age,cust_id))
        conn.commit()
        clear()
    else:
        return True


conn=sqlite3.connect('customer.db')
cursor=conn.cursor()


app=tk.Tk()
q=tk.StringVar()
t1=tk.StringVar()
t2=tk.StringVar()
t3=tk.StringVar()
t4=tk.StringVar()

wrapper1=tk.LabelFrame(app,text='Customer List')
wrapper2=tk.LabelFrame(app,text='Search')
wrapper3=tk.LabelFrame(app,text='Customer Data')

wrapper1.pack(fill=tk.BOTH,expand=1,padx=20,pady=10)
wrapper2.pack(fill=tk.BOTH,expand=1,padx=20,pady=10)
wrapper3.pack(fill=tk.BOTH,expand=1,padx=20,pady=10)

tree=ttk.Treeview(wrapper1,columns=(1,2,3,4),show='headings',height='6')
tree.column(1,anchor=tk.CENTER)
tree.column(2,anchor=tk.CENTER)
tree.column(3,anchor=tk.CENTER)
tree.column(4,anchor=tk.CENTER)
tree.pack(fill=tk.BOTH,expand=1)
tree.heading(1,text='CUSTOMER ID')
tree.heading(2,text='FIRST NAME')
tree.heading(3,text='LAST NAME')
tree.heading(4,text='AGE')
tree.bind('<Double 1>',getrow)



query="SELECT customer_id,first_name,last_name,age from customers"
cursor.execute(query)
rows=cursor.fetchall()
update(rows)

#search area
lbl=tk.Label(wrapper2,text='Search')
lbl.pack(side=tk.LEFT,padx=10)
ent=tk.Entry(wrapper2,textvariable=q)
ent.pack(side=tk.LEFT,padx=6)
btn=tk.Button(wrapper2,text='search',command=search)
btn.pack(side=tk.LEFT,padx=6)
cbtn=tk.Button(wrapper2,text='Clear',command=clear)
cbtn.pack(side=tk.LEFT,padx=6)

#user data section
lbl1=tk.Label(wrapper3,text='Customer ID')
lbl1.grid(row=0,column=0,padx=5,pady=3)
ent1=tk.Entry(wrapper3,textvariable=t1)
ent1.grid(row=0,column=1,padx=5,pady=3)
lbl2=tk.Label(wrapper3,text='First Name')
lbl2.grid(row=1,column=0,padx=5,pady=3)
ent2=tk.Entry(wrapper3,textvariable=t2)
ent2.grid(row=1,column=1,padx=5,pady=3)
lb13=tk.Label(wrapper3,text='Last Name')
lb13.grid(row=2,column=0,padx=5,pady=3)
ent3=tk.Entry(wrapper3,textvariable=t3)
ent3.grid(row=2,column=1,padx=5,pady=3)
lbl4=tk.Label(wrapper3,text='Age')
lbl4.grid(row=3,column=0)
ent4=tk.Entry(wrapper3,textvariable=t4)
ent4.grid(row=3,column=1,padx=5,pady=3)
add_btn=tk.Button(wrapper3,text='Add New',command=add_new)
add_btn.grid(row=4,column=0,padx=5,pady=3)
up_btn=tk.Button(wrapper3,text='Update',command=update_customer)
up_btn.grid(row=4,column=1,padx=5,pady=3)
del_btn=tk.Button(wrapper3,text='Delete',command=delete_customer)
del_btn.grid(row=4,column=2,padx=5,pady=3)


app.title('My Application')
app.geometry('800x700')
app.mainloop()