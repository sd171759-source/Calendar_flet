
import flet as ft
from SetCalendar import SetCalendar
from settings import Config, CustomTitleText
from storage import BirthdayStorage

def main(page: ft.Page):



    page.title = Config.WINDOW_TITLE
    page.bgcolor = Config.APP_BACKGROUND

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = ft.Padding.all(20)
    page.scroll = ft.ScrollMode.AUTO
    page.window_prevent_close = True



    storage = BirthdayStorage()
    ui_title = CustomTitleText(" Календарь Именинников" )
    ui_hint = ft.Text("Кликните на ячейку даты для добавления или редактирования", italic=True, color="#EFF4bd")
    ui_calendar = SetCalendar(storage=storage)


    page.add(
        ft.Column(
            controls=[
                ui_title,
                ui_hint,
                ft.Divider(color=Config.PRIMARY_COLOR),
                ui_calendar,
                ft.Divider(color="white10"),

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
