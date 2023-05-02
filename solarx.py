from gpiozero import LightSensor
import flet as ft
import yagmail
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

moneyGenerated = 0

async def main(page: ft.Page):
    
    async def btnAreaClick(e):
        ldr = LightSensor(27)

        total = 0

        for i in range(1,10):
            total += (ldr.value * 1000000)
            lvLDR.controls.append(ft.Text(str(ldr.value)))
            asyncio.sleep(1)
            page.update_async()
            
        current = 0.0000026455026
        resistance = 1000000 - (total / 10)
        power = current * current * resistance
        powerPerSqMetre = power / 0.00000012
        
        area = tbArea.value
        finalValue = int(area) * powerPerSqMetre
        finalValuekW = finalValue / 1000
        moneyGenerated = (finalValuekW * (10/(60*60))) * 16
        await page.add_async(ft.Text(f"Money made in 10s: {str(moneyGenerated)} pence."))
    
    async def btnEmailClick(e):
            yag = yagmail.SMTP(tbEmail.value, tbPassword.value)
            yag.send(tbRecipient.value, "SolarX Results", f"You will make {str(moneyGenerated)} pence every 10 seconds!.")
            await page.add_async(ft.Text("Email sent!"))
        
    page.title = "SolarX"
    page.window_width = 700
    page.window_height = 400
    page.window_resizable = False
    page.scroll = ft.ScrollMode(value="auto")
    
    page.appbar = ft.AppBar(
        title=ft.Text("SolarX"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT
    )
    
    tbArea = ft.TextField(
        label="Area of solar panels (m²): "
    )
    
    btnArea = ft.ElevatedButton(
        text="Calculate", 
        on_click=btnAreaClick
    )
    
    tbEmail = ft.TextField(
        label="Enter your gmail username: "
    )
    
    tbPassword = ft.TextField(
        label="Enter your password: ", 
        password=True, 
        can_reveal_password=True
    )
    
    tbRecipient = ft.TextField(
        label="Enter the recipient's email address: ",
    )
    
    btnEmail = ft.ElevatedButton(
        text="Send Email", 
        on_click=btnEmailClick
    )
    
    lvLDR = ft.ListView( 
        spacing=10, 
        padding=20, 
        auto_scroll=True,
        height=100
    )
    
    await page.add_async(
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
            ]),
            ft.Column(controls=[
                lvLDR
            ])
        ])
    )
    
    pass

ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets")