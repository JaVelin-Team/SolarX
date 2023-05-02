from gpiozero import LightSensor
import time
import flet as ft
import yagmail

def main(page: ft.Page):
    
    def btnAreaClick(e):
        ldr = LightSensor(27)

        total = 0

        for i in range(1,10):
            total += (ldr.value * 1000000)
            print(ldr.value)
            time.sleep(1)
            
        current = 0.0000026455026
        resistance = 1000000 - (total / 10)
        power = current * current * resistance
        powerPerSqMetre = power / 0.00000012
        
        area = tbArea.value
        finalValue = int(area) * powerPerSqMetre
        finalValuekW = finalValue / 1000
        moneyGenerated = (finalValuekW * (10/(60*60))) * 16
        page.add(ft.Text(f"Money made in 10s: {str(moneyGenerated)} pence."))
        return moneyGenerated
    
    def btnEmailClick(e, moneyGenerated):
            yag = yagmail.SMTP(tbEmail.value, tbPassword.value)
            yag.send(tbRecipient.value, "SolarX Results", f"You will make {str(moneyGenerated)} pence every 10 seconds!.")
            page.add(ft.Text("Email sent!"))

    page.title = "SolarX"
    page.window_width = 700
    page.window_height = 700
    page.window_resizable = False
    
    img = ft.Image(
        src="public\cover.png",
        width=700,
        fit=ft.ImageFit.CONTAIN,
    )
    
    images = ft.Row(
        expand=1, 
        wrap=False, 
        scroll="always"
        )
    
    tbArea = ft.TextField(
        label="Area of solar panels (m^2): "
        )
    
    btnArea = ft.ElevatedButton(
        text="Calculate", 
        on_click=btnAreaClick
        )
    
    tbEmail = ft.TextField(
        label="Enter your email username: "
        )
    
    tbPassword = ft.TextField(
        label="Enter your password: ", 
        password=True, 
        can_reveal_password=True
        )
    
    tbRecipient = ft.TextField(
        label="Enter the recipient's email address: ",
        suffix_text="@gmail.com"
        )
    
    btnEmail = ft.ElevatedButton(
        text="Send Email", 
        on_click=btnEmailClick
        )
    
    page.add(
        img, 
        images,
        ft.Row(controls=[
            ft.Column(controls=[
            tbArea, 
            btnArea
            ]),
            ft.Column(controls=[
                tbEmail,
                tbPassword,
                tbRecipient,
                btnEmail
            ])
        ])
    )
    
    pass

ft.app(target=main)