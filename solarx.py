from gpiozero import LightSensor
import time
import yagmail
from tkinter import *

def btnClick():
    area = int(ent.get())
    finalValue = area * powerPerSqMetre
    finalValuekW = finalValue / 1000
    moneyGenerated = (finalValuekW * (10/(60*60))) * 16
    lblMoney.config(text=f"Money made in 10s: {str(moneyGenerated)} pence.")
    
def btnSendClick():
    yag = yagmail.SMTP(entEmail.get())
    yag.send(entRecipient.get(), entSubject.get(), entBody.get())
    

root = Tk()
root.title("SolarX")
root.geometry("700x500")
root.iconbitmap("public\icon.ico")

ent = Entry()
ent.place(x=10, y=50)

lbl = Label(text="Enter the area of solar panels you wish to install (m^2): ", font=("Arial", 10, "bold"))
lbl.place(x=10, y=10)

btn = Button(text="Calculate", font=("Arial", 10, "bold"), command=btnClick)
btn.place(x=200, y=45)

lblMoney = Label(text="Press the button to find out how much money you could make!", font=("Arial", 10, "bold"))
lblMoney.place(x=10,y=80)

lblLDR = Label(text="LDR Value: ", font=("Arial", 10, "bold"))
lblLDR.place(x=500, y=10)

lstbx = Listbox(width=30, height=20)
lstbx.place(x=500,y=30)

lblEmail = Label(text="Enter your email address: ", font=("Arial", 10, "bold"))
lblEmail.place(x=10, y=120)

entEmail = Entry()
entEmail.place(x=10, y=150)

lblRecipient = Label(text="Enter the recipient's email address: ", font=("Arial", 10, "bold"))
lblRecipient.place(x=10, y=180)

entRecipient = Entry()
entRecipient.place(x=10, y=210)

lblSubject = Label(text="Enter the subject of the email: ", font=("Arial", 10, "bold"))
lblSubject.place(x=10, y=240)

entSubject = Entry()
entSubject.place(x=10, y=270)

lblBody = Label(text="Enter the body of the email: ", font=("Arial", 10, "bold"))
lblBody.place(x=10, y=300)

entBody = Text(width=50, height=5)
entBody.place(x=10, y=330)

btnSend = Button(text="Send Email", font=("Arial", 10, "bold"), command=btnSendClick)
btnSend.place(x=10, y=450)

ldr = LightSensor(27)

total = 0

for i in range(1,10):
    total += (ldr.value * 1000000)
    lstbx.insert(ldr.value)
    time.sleep(1)
    
current = 0.0000026455026
resistance = 1000000 - (total / 10)
power = current * current * resistance
powerPerSqMetre = power / 0.00000012

root.mainloop()