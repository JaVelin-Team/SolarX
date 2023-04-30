from gpiozero import LightSensor
import time
import yagmail

# a variable with the LDR reading pin number
ldr = LightSensor(27)

total = 0

for i in range(1,10):
    total += (ldr.value * 1000000) # resistance in ohms
    print(ldr.value)
    time.sleep(1) # time to wait in seconds

# calculating power per square metre using the ldr
current = 0.0000026455026 # current through the ldr
resistance = 1000000 - (total / 10) # average resistance through the ldr, taking into account resistance decreases when light intensity increases
power = current * current * resistance # power from the ldr
powerPerSqMetre = power / 0.00000012 # the power divided by the surface area of the ldr

# 16p per kWh when selling power to the national grid

# finding the power generated for the surface area of the customers roof
area = int(input("Enter the area of your roof in m^2 which could accomodate solar panels: "))
finalValue = area * powerPerSqMetre
finalValuekW = finalValue / 1000 # converting to kW
    
moneyGenerated = (finalValuekW * (10/(60*60))) * 16 # convewrting to kWh then to the money made
print(f"Money made in 10s: {str(moneyGenerated)} pence")

# EMAIL SENDER:

# starting a connection
yag = yagmail.SMTP("sender's gmail username", "sender's gmail password")

# defining variables
to = "recipient email"
subject = "Money you could have made with solar panels!"
body = f"Money made in 10s: {str(moneyGenerated)} pence"

# sending the email
yag.send(to, subject, body)
print("Email Sent")
