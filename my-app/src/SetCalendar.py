import calendar
import flet as ft
import datetime
from settings import Config, CustomCalendarCell, CustomTitleText
from dialogs import BirthdayDialog

class SetCalendar(ft.Container):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage
        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month

        self.calendar_grid = ft.Column( # сетка календаря ( дни и числа)
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.navigation_row = ft.Row( # навигация сверху
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=Config.CELL_WIDTH *7
        )

        self.content = ft.Column(
            controls=[self.navigation_row, self.calendar_grid],
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
        )

    def did_mount(self):
        self.create_month_calendar()
        self.update()

    def change_month(self, delta):
        self.current_month += delta
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.refresh_after_save()

    def refresh_after_save(self):
        self.create_month_calendar()
        self.update()

    def open_birthday_dialog(self, month, day):
        BirthdayDialog(self.page, self.storage, month, day, self.refresh_after_save)

    def create_month_calendar(self):
        month_name = calendar.month_name[self.current_month]
        month_label = CustomTitleText(f"{month_name} {self.current_year}")

        self.navigation_row.controls = [
            ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, on_click=lambda n: self.change_month(-1)),
            month_label,
            ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, on_click=lambda n: self.change_month(1)),
        ]

        self.calendar_grid.controls = []
        month_grid = ft.Column(alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                               spacing=5)

        weekday_labels = [
            ft.Container(width=Config.CELL_WIDTH, height=100, alignment=ft.Alignment.CENTER,
                         content=ft.Text(day, size=20, color=Config.DAYS_COLOR , weight=ft.FontWeight.BOLD))
            for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        ]
        month_grid.controls.append(ft.Row(controls=weekday_labels, alignment=ft.MainAxisAlignment.CENTER, spacing=15))

        month_matrix = calendar.monthcalendar(self.current_year, self.current_month)
        today = datetime.date.today()

        for week in month_matrix:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=15)
            for day in week:
                day_text = str(day) if day != 0 else ""
                if day == 0:
                    week_row.controls.append(ft.Container(width=Config.CELL_WIDTH, height=Config.CELL_HEIGHT))
                    continue

                date_key = f"{self.current_month:02d}-{day:02d}"
                record = self.storage.birthday_map.get(date_key)
                has_birthday = record is not None

                is_today = (day == today.day and self.current_month == today.month and self.current_year == today.year)
                bg = Config.BIRTHDAY_BG_COLOR if has_birthday else (
                    Config.TODAY_BG_COLOR if is_today else Config.CELL_BG_COLOR)

                cell_content = ft.Column(alignment=ft.MainAxisAlignment.CENTER,
                                         horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                cell_content.controls.append(ft.Text(day_text, color=Config.DAYS_COLOR if (is_today or has_birthday) else Config.EVERYDAY_COLOR,
                                                     weight=ft.FontWeight.BOLD if (is_today or has_birthday) else None,
                                                     size=14))

                if has_birthday:
                    cell_content.controls.append(
                        ft.Text(record.name, size=14, color="white", weight=ft.FontWeight.BOLD,
                                overflow=ft.TextOverflow.ELLIPSIS, text_align=ft.TextAlign.CENTER))


                day_cell = CustomCalendarCell(content=cell_content, bg_color=bg,
                                              on_click=lambda n, m=self.current_month, d=day: self.open_birthday_dialog(
                                                  m, d))
                week_row.controls.append(day_cell)
            month_grid.controls.append(week_row)

        self.calendar_grid.controls.append(month_grid)
