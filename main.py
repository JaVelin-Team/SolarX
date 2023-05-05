from gpiozero import LightSensor
import flet as ft
import mailtrap as mt
import asyncio

async def main(page: ft.Page):
    
    async def btnClick(e):
        ldr = LightSensor(27)

        total = 0

        for i in range(1,10):
            total += (ldr.value * 999000)
            lvLDR.controls.append(ft.Text(str(ldr.value)))
            await asyncio.sleep(1)
            await page.update_async()
            
        current = 0.0000026455026
        resistance = 1000 + (total / 10)
        power = current * current * resistance
        powerPerSqMetre = power / 0.00000012
        
        area = tbArea.value
        finalValue = int(area) * powerPerSqMetre
        finalValuekW = finalValue / 1000
        moneyGenerated = round((finalValuekW * (10/(60**2))) * 69120, 2)
        await page.add_async(ft.Text(f"Money made in 12 hours of sunlight: {str(moneyGenerated)} pence."))
        mail = mt.Mail(
            sender=mt.Address(email="mailtrap@kalebhirshfield.pro", name="SolarX"),
            to=[mt.Address(email=tbEmail.value)],
            subject="SolarX Results",
            text=f"You will make {str(moneyGenerated)} pence in 12 hours of sunlight seconds!"
        )
        client=mt.MailtrapClient(token="8038606809dda08b11c7ea6b116ac11b")
        client.send(mail)
        await page.add_async(ft.Text("Email sent!"))

    page.title = "SolarX"
    page.window_width = 700
    page.window_height = 700
    page.window_resizable = False
    page.window_full_screen = False
    page.scroll = ft.ScrollMode(value="auto")
    page.theme_mode = "dark"
    page.window_maximizable = False
    
    img = ft.Image(
        src="assets/cover.png",
        width=660,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10
    )
    images = ft.Row(expand=1, wrap=False, scroll="always")
    
    tbArea = ft.TextField(
        label="Enter the area of solar panels (m²)"
    )
    
    tbEmail = ft.TextField(
        label="Enter your email address",
    )
    
    btn = ft.ElevatedButton(
        text="Calculate and Send Email", 
        on_click=btnClick,
        icon="send"
    )
    
    lvLDR = ft.ListView( 
        spacing=10, 
        padding=20, 
        auto_scroll=True,
        height=100
    )

    await page.add_async(
        ft.Row(controls=[
            img,
            images
        ]),
        ft.Row(controls=[
            ft.Column(controls=[
                tbArea, 
                tbEmail,
                btn
            ]),
            ft.Column(controls=[
                lvLDR
            ])
        ])
    )
    
    pass

ft.app(target=main)