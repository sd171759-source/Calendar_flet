import flet as ft

class Config:

    JSON_FILE = "birthdays.json"
    CELL_WIDTH = 100
    CELL_HEIGHT = 100
    CELL_BG_COLOR = "white10"
    TODAY_BG_COLOR = "#bdecb6"
    BIRTHDAY_BG_COLOR = "#ff9214"
    PRIMARY_COLOR = "green400"
    WINDOW_TITLE = "Календарь Дней Рождения"
    APP_BACKGROUND = "#0A3323"
    DAYS_COLOR ="#faeedd"
    EVERYDAY_COLOR ="#eceabe"




class CustomTitleText(ft.Text): # шрифт для заголовка
    def __init__(self, text: str, **kwargs):
        super().__init__(value=text, size=18, weight=ft.FontWeight.BOLD, color=Config.PRIMARY_COLOR, **kwargs)

class CustomInputField(ft.TextField): # текстовое поле
    def __init__(self, label: str, value: str = "", **kwargs):
        super().__init__(label=label, value=value, border_color=Config.PRIMARY_COLOR, focused_border_color="yellow", **kwargs)

class CustomActionButton(ft.ElevatedButton): # кнопка
    def __init__(self, text: str, on_click, **kwargs):
        super().__init__(text, on_click=on_click, bgcolor=Config.PRIMARY_COLOR, color="white",
                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), **kwargs)

class CustomCalendarCell(ft.Container): # ячейка календаря
    def __init__(self, content, bg_color, on_click, **kwargs):
        super().__init__(
            content=content, width=Config.CELL_WIDTH, height=Config.CELL_HEIGHT,
            bgcolor=bg_color, border_radius=8, alignment=ft.Alignment.CENTER, on_click=on_click,
            **kwargs)


