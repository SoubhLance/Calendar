from tkinter import *
import calendar


#making the main window
root= Tk()
root.title("Calender")
root.geometry("240x200")
root.resizable(0,0)
root.configure(bg="light Grey")

#Function for displaying
def Show():
    a= int(spin1.get())
    b= int(spin2.get())

    cal= calendar.month(b,a)
    
    txt.delete(0.0,END)
    txt.insert(INSERT,cal)


lbl1=Label(root,text="Month",font=('arial',9,'bold'),bg="light grey").place(x=15,y=0)
lbl2=Label(root,text="Year",font=('arial',9,'bold'),bg="light grey").place(x=115,y=0)

#creating spinbox

spin1=Spinbox(root,values=(1,2,3,4,5,6,7,8,9,10,11,12),width=4)
spin1.place(x=60,y=0)



spin2 = Spinbox(root,from_=1999,to_=2100,width=4)
spin2.place(x=150,y=0)

#Creating the Button

btn= Button(root,text="Show",font=('arial',9,'bold'),command=Show).place(x=100,y=30)


#Dsplaying wuith the text box
txt=Text(root,width=24,height=8)
txt.place(x=20,y=57)

root.mainloop()