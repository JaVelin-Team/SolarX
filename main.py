from gpiozero import LightSensor
import flet as ft
from flet import RoundedRectangleBorder
import time
import mailtrap as mt
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def main(page: ft.Page):
    def closeBanner(_):
        page.banner.open = False
        page.update()

    def btnClick(_):
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
                text=f"You will make {str(moneyGenerated)}p in 12 hours of sunlight!",
            )
            client = mt.MailtrapClient(token=getenv("MAILTRAP_TOKEN"))
            client.send(mail)

            def closeBs(_):
                bs.open = False
                bs.update()

            bs = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(
                                f"You will make {str(moneyGenerated)}p in 12 hours of sunlight!",
                                size=20,
                            ),
                            ft.TextButton(
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
    page.window_width = 336
    page.window_height = 218
    page.window_resizable = False
    page.window_full_screen = False
    page.scroll = ft.ScrollMode(value="auto")
    page.theme_mode = "dark"
    page.window_maximizable = False
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    windowDragArea = ft.WindowDragArea(
        ft.Container(
            ft.Text("SolarX", text_align="center", color=ft.colors.WHITE70),
            bgcolor=ft.colors.BLACK54,
            padding=10,
            border_radius=10,
        ),
        expand=True,
        maximizable=False,
    )

    style = ft.ButtonStyle(
        color={
            ft.MaterialState.DEFAULT: ft.colors.WHITE70,
        },
        shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
        bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLACK54},
    )

    btnClose = ft.IconButton(
        ft.icons.CLOSE,
        style=ft.ButtonStyle(
            color={
                ft.MaterialState.DEFAULT: ft.colors.WHITE70,
                ft.MaterialState.HOVERED: ft.colors.RED_ACCENT_200,
            },
            bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLACK54},
            shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
        ),
        on_click=lambda _: page.window_close(),
    )

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
        label="Solar panel area (m²)",
        keyboard_type="number",
        border_radius=10,
        border_color=ft.colors.BACKGROUND,
        text_style=ft.TextStyle(color=ft.colors.WHITE70),
        label_style=ft.TextStyle(color=ft.colors.WHITE70),
        border_width=2,
        focused_border_width=4,
        on_submit=btnClick,
        autofocus=True,
        focused_border_color=ft.colors.PINK_ACCENT_400,
        bgcolor=ft.colors.BLACK54,
        focused_bgcolor=ft.colors.BLACK12,
        cursor_color=ft.colors.PINK_ACCENT_400,
        cursor_width=3,
    )

    tbEmail = ft.TextField(
        label="Email address",
        keyboard_type="email",
        border_radius=10,
        border_color=ft.colors.BACKGROUND,
        text_style=ft.TextStyle(color=ft.colors.WHITE70),
        label_style=ft.TextStyle(color=ft.colors.WHITE70),
        border_width=2,
        focused_border_width=4,
        on_submit=btnClick,
        focused_border_color=ft.colors.ORANGE_ACCENT_400,
        bgcolor=ft.colors.BLACK54,
        focused_bgcolor=ft.colors.BLACK12,
        suffix_icon=ft.icons.SEND_SHARP,
        cursor_color=ft.colors.ORANGE_ACCENT_400,
        cursor_width=3,
    )

    page.add(
        ft.Row(controls=[windowDragArea, btnClose]),
        ft.Row(controls=[tbArea]),
        ft.Row(controls=[tbEmail]),
    )

    pass


ft.app(target=main)
