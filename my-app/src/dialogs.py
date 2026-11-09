import flet as ft
import calendar
from settings import CustomInputField, CustomActionButton, CustomTitleText
from storage import BirthdayRecord


class BirthdayDialog:
    def __init__(self, page: ft.Page, storage, month, day, on_save_callback):
        self.page = page
        self.storage = storage
        self.on_save = on_save_callback
        self.date_key = f"{month:02d}-{day:02d}"
        self.existing_record = self.storage.birthday_map.get(self.date_key)

        self.name_input = CustomInputField(
            label="Имя именинника",
            value=self.existing_record.name if self.existing_record else "",
            multiline=True


        )
        self.comment_input = CustomInputField(
            label="Комментарий (заметка)",
            value=self.existing_record.comment if self.existing_record else "",
            multiline=True # многострочность
        )


        self.dialog = ft.AlertDialog(
            title=CustomTitleText(f"День рождения {day} {calendar.month_name[month]}"),
            content=ft.Column(controls=[self.name_input, self.comment_input], tight=True, spacing=30),
            actions=[
                ft.TextButton("Удалить", icon=ft.Icons.DELETE, icon_color="red", on_click=self.delete_click),
                ft.TextButton("Отмена", on_click=lambda n: self.close_dialog()),
                CustomActionButton("Сохранить", on_click=self.save_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.dialog.open = False
        self.page.update()

    def save_click(self, e):
        name_val = self.name_input.value.strip()
        comment_val = self.comment_input.value.strip()

        if name_val:
            new_record = BirthdayRecord(name=name_val, comment=comment_val, date_str=self.date_key)
            self.storage.birthday_map.put(self.date_key, new_record) # добавление записи
        else:
            self.storage.birthday_map.remove(self.date_key) # удаление записи

        self.storage.save_birthdays()
        self.close_dialog()
        self.on_save()

    def delete_click(self, e):
        self.storage.birthday_map.remove(self.date_key)
        self.storage.save_birthdays()
        self.close_dialog()
        self.on_save()
