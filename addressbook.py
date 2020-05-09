from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import sqlite3
from tkinter import messagebox

root= Tk()
root.title('Checkboxes')
root.geometry("400x400")

#Create/ Connect to a database
conn = sqlite3.connect('address_book.db')

#Create cursor
c = conn.cursor()

#Create Table. Delete Code after initial run
"""
c.execute(''' 
	CREATE TABLE addresses(
		first_name text,
		last_name text,
		address text,
		city text,
		state text,
		zipcode integer
	)''')
"""
def update():
	conn = sqlite3.connect('address_book.db')
	c = conn.cursor()
	record_id=select_box.get()
	
	c.execute("""
		UPDATE addresses SET
		first_name = :first,
		last_name = :last,
		address = :address,
		city = :city,
		state = :state,
		zipcode= :zipcode
		WHERE oid =:oid""",
		{
				'first': f_name_editor.get(),
				'last': l_name_editor.get(),
				'address': address_editor.get(),
				'city': city_editor.get(),
				'state': state_editor.get(),
				'zipcode': zipcode_editor.get(),
				'oid':record_id
			}
		)
	
	conn.commit()
	conn.close()
 
	editor.destroy()
	response = messagebox.showinfo("Success","Record Updated")
	select_box.delete(0,END)


#Function to Update a record
def edit():
	global editor
	editor= Tk()
	editor.title('Update a Record')
	editor.geometry("400x300")

	conn = sqlite3.connect('address_book.db')
	c = conn.cursor()

	record_id = select_box.get()

	c.execute("SELECT * FROM addresses where oid = "+record_id)
	records = c.fetchall()
	#Create Global Variables 
	global f_name_editor
	global l_name_editor
	global address_editor
	global city_editor
	global state_editor
	global zipcode_editor
	#Create Text Boxes
	f_name_editor = Entry(editor,width=30)
	f_name_editor.grid(row=0,column=1,padx=20,pady=(10,0))

	l_name_editor = Entry(editor,width=30)
	l_name_editor.grid(row=1,column=1)

	address_editor = Entry(editor,width=30)
	address_editor.grid(row=2,column=1)

	city_editor = Entry(editor,width=30)
	city_editor.grid(row=3,column=1)

	state_editor = Entry(editor,width=30)
	state_editor.grid(row=4,column=1)

	zipcode_editor = Entry(editor,width=30)
	zipcode_editor.grid(row=5,column=1)


	#Create Text Box Labels
	f_name_label = Label(editor,text="First Name")
	f_name_label.grid(row=0,column=0,pady=(10,0))

	l_name_label = Label(editor,text="Last Name")
	l_name_label.grid(row=1,column=0)

	address_label = Label(editor,text="Address")
	address_label.grid(row=2,column=0)

	city_label = Label(editor,text="City")
	city_label.grid(row=3,column=0)

	state_label = Label(editor,text="State")
	state_label.grid(row=4,column=0)

	zipcode_label = Label(editor,text="Zipcode")
	zipcode_label.grid(row=5,column=0)

	#Loop Through Results
	for record in records:
		f_name_editor.insert(0,record[0])
		l_name_editor.insert(0,record[1])
		address_editor.insert(0,record[2])
		city_editor.insert(0,record[3])
		state_editor.insert(0,record[4])
		zipcode_editor.insert(0,record[5])

	save_button=Button(editor,text="Save Record",command=update)
	save_button.grid(row=6, column=0,columnspan=2,padx=10,pady=10,ipadx=137)

#Function to delete a record
def delete():
	conn = sqlite3.connect('address_book.db')
	c = conn.cursor()

	c.execute("DELETE from addresses WHERE oid="+select_box.get())

	select_box.delete(0,END)
	conn.commit()
	conn.close()
	response = messagebox.showinfo("Success","Record Deleted")

#Create Submit Function
def submit():

	conn = sqlite3.connect('address_book.db')
	c = conn.cursor()

	#Insert Into Table
	c.execute("INSERT INTO addresses VALUES(:f_name, :l_name, :address, :city, :state, :zipcode)",
			{
				'f_name': f_name.get(),
				'l_name': l_name.get(),
				'address': address.get(),
				'city': city.get(),
				'state': state.get(),
				'zipcode': zipcode.get()
			})

	conn.commit()
	conn.close()

	#Clear the text Boxes
	f_name.delete(0,END)
	l_name.delete(0,END)
	address.delete(0,END)
	city.delete(0,END)
	state.delete(0,END)
	zipcode.delete(0,END)

	response = messagebox.showinfo("Success","Record Added")

def query():
	conn = sqlite3.connect('address_book.db')
	c = conn.cursor()

	c.execute("SELECT *,oid FROM addresses")
	records = c.fetchall()
	#print(records)

	#Loop through results
	print_records=''
	for record in records:
		print_records += str(record[0]) +" "+ str(record[1])+"\t"+ str(record[6]) +"\n"

	query_label=Label(root,text=print_records)
	query_label.grid(row=13,column=0,columnspan=2)

	conn.commit()
	conn.close()

#Create Text Boxes
f_name = Entry(root,width=30)
f_name.grid(row=0,column=1,padx=20,pady=(10,0))

l_name = Entry(root,width=30)
l_name.grid(row=1,column=1)

address = Entry(root,width=30)
address.grid(row=2,column=1)

city = Entry(root,width=30)
city.grid(row=3,column=1)

state = Entry(root,width=30)
state.grid(row=4,column=1)

zipcode = Entry(root,width=30)
zipcode.grid(row=5,column=1)

select_box = Entry(root,width=30)
select_box.grid(row=10,column=1,pady=10)

#Create Text Box Labels
f_name_label = Label(root,text="First Name")
f_name_label.grid(row=0,column=0,pady=(10,0))

l_name_label = Label(root,text="Last Name")
l_name_label.grid(row=1,column=0)

address_label = Label(root,text="Address")
address_label.grid(row=2,column=0)

city_label = Label(root,text="City")
city_label.grid(row=3,column=0)

state_label = Label(root,text="State")
state_label.grid(row=4,column=0)

zipcode_label = Label(root,text="Zipcode")
zipcode_label.grid(row=5,column=0)

select_label = Label(root,text="ID Number")
select_label.grid(row=10,column=0,pady=10)


#Create Submit button
submit_btn = Button(root,text="Add record to Database",command=submit)
submit_btn.grid(row=6,column=0,columnspan=2,pady=10,padx=10,ipadx=112)

#Query Button
query_button=Button(root,text="Show Records",command=query)
query_button.grid(row=7, column=0,columnspan=2,padx=10,pady=10,ipadx=137)

#Create A Delete Button
delete_button=Button(root,text="Delete Record",command=delete)
delete_button.grid(row=11, column=0,columnspan=2,padx=10,pady=10,ipadx=137)

#Create An Update Button
edit_button=Button(root,text="Update Record",command=edit)
edit_button.grid(row=12, column=0,columnspan=2,padx=10,pady=10,ipadx=137)

#Commit Changes
conn.commit()

#Close Connection
conn.close()

root.mainloop()
