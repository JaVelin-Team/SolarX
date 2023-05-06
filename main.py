from gpiozero import LightSensor
import flet as ft
from flet import RoundedRectangleBorder
import time
import mailtrap as mt


def main(page: ft.Page):
    def btnClick(e):
        ldr = LightSensor(27)

        total = 0

        for i in range(1, 10):
            total += ldr.value * 999000
            time.sleep(1)

        current = 0.0000026455026
        resistance = 1000 + (total / 10)
        power = current * current * resistance
        powerPerSqMetre = power / 0.00000012

        area = tbArea.value
        finalValue = int(area) * powerPerSqMetre
        finalValuekW = finalValue / 1000
        moneyGenerated = round((finalValuekW * (10 / (60**2))) * 69120, 2)

        mail = mt.Mail(
            sender=mt.Address(email="mailtrap@kalebhirshfield.pro", name="SolarX"),
            to=[mt.Address(email=tbEmail.value)],
            subject="SolarX Results",
            text=f"You will make {str(moneyGenerated)}p in 12 hours of sunlight seconds!",
        )
        client = mt.MailtrapClient(token="8038606809dda08b11c7ea6b116ac11b")
        client.send(mail)

        btn.update(
            ft.Text(
                f"Money made in 12 hours of sunlight: {str(moneyGenerated)}p, email sent!"
            )
        )

    page.title = "SolarX"
    page.window_width = 645
    page.window_height = 455
    page.window_resizable = False
    page.window_full_screen = False
    page.scroll = ft.ScrollMode(value="auto")
    page.theme_mode = "dark"
    page.window_maximizable = False
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    windowDragArea = ft.WindowDragArea(
        ft.Container(ft.Text("SolarX"), bgcolor=ft.colors.BACKGROUND, padding=10),
        expand=True,
        maximizable=False,
    )

    btnClose = ft.IconButton(ft.icons.CLOSE, on_click=lambda e: page.window_close())

    img = ft.Image(
        src="assets/cover.png", width=610, fit=ft.ImageFit.CONTAIN, border_radius=10
    )
    images = ft.Row(expand=1, wrap=False, scroll="always")

    tbArea = ft.TextField(
        label="Enter the area of solar panels (m²)",
        keyboard_type="number",
        border_radius=10,
        border_color=ft.colors.WHITE60,
        text_style=ft.TextStyle(color=ft.colors.WHITE60),
        cursor_color=ft.colors.WHITE60,
    )

    tbEmail = ft.TextField(
        label="Enter your email address",
        keyboard_type="email",
        border_radius=10,
        border_color=ft.colors.WHITE60,
        text_style=ft.TextStyle(color=ft.colors.WHITE60),
        cursor_color=ft.colors.WHITE60,
    )

    style = ft.ButtonStyle(
        color={
            ft.MaterialState.DEFAULT: ft.colors.WHITE60,
        },
        shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
    )

    btn = ft.OutlinedButton(
        text="Calculate and Send Email",
        on_click=btnClick,
        icon="send",
        icon_color=ft.colors.WHITE60,
        style=style,
        expand=True,
    )

    page.add(
        ft.Row(controls=[windowDragArea, btnClose]),
        ft.Row(controls=[img, images]),
        ft.Row(controls=[tbArea, tbEmail]),
        ft.Row(controls=[btn]),
    ),

    pass


ft.app(target=main)
