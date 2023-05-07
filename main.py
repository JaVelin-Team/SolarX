from gpiozero import LightSensor
import flet as ft
from flet import RoundedRectangleBorder
import time
import mailtrap as mt


def main(page: ft.Page):
    def closeBanner(e):
        page.banner.open = False
        page.update()

    def btnClick(e):
        try:
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
            moneyGenerated = round((finalValuekW * (691200 / (60**2))), 2)

            mail = mt.Mail(
                sender=mt.Address(email="mailtrap@kalebhirshfield.pro", name="SolarX"),
                to=[mt.Address(email=tbEmail.value)],
                subject="SolarX Results",
                text=f"You will make {str(moneyGenerated)}p in 12 hours of sunlight seconds!",
            )
            client = mt.MailtrapClient(token="8038606809dda08b11c7ea6b116ac11b")
            client.send(mail)

            def closeBs(e):
                bs.open = False
                bs.update()

            bs = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(
                                f"You will make {str(moneyGenerated)}p in 12 hours of sunlight seconds!",
                                size=20,
                            ),
                            ft.OutlinedButton(
                                "Close bottom sheet", on_click=closeBs, style=style
                            ),
                        ],
                        tight=True,
                    ),
                    padding=10,
                ),
                open=True,
            )
            page.add(bs)

        except:
            page.banner.open = True
            page.update()

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

    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_ACCENT_700,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.BLACK, size=40),
        content=ft.Text(
            color=ft.colors.BLACK,
            value="Oops, we were unable to find LDR values or send an email. Please try again.",
        ),
        actions=[
            ft.TextButton(
                "Retry",
                on_click=btnClick,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: ft.colors.BLACK,
                    },
                    bgcolor={
                        ft.MaterialState.HOVERED: ft.colors.AMBER_ACCENT_400,
                    },
                    shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
                ),
            ),
            ft.TextButton(
                "Cancel",
                on_click=closeBanner,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: ft.colors.BLACK,
                    },
                    bgcolor={
                        ft.MaterialState.HOVERED: ft.colors.AMBER_ACCENT_400,
                    },
                    shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
                ),
            ),
        ],
    )

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
