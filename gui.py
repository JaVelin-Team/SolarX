import flet as ft


def main(page: ft.Page):
    
    def btnClick(e):
        powerPerSqMetre = 1000
        area = ft.TextField.data
        finalValue = area * powerPerSqMetre
        finalValuekW = finalValue / 1000
        moneyGenerated = (finalValuekW * (10/(60*60))) * 16
        page.add(ft.Text(f"Money made in 10s: {str(moneyGenerated)} pence."))
        return moneyGenerated

    page.title = "SolarX"
    ft.icon = "public/icon.ico"
    page.add(
        ft.Column(controls=[
            ft.TextField(label="Area of solar panels (m^2): "),
            ft.ElevatedButton(text="Calculate", on_click=btnClick),
            
    ])
)
    pass

ft.app(target=main)