from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable

import flet as ft

from utils import Observable


class TimeCard(ft.Container):
    def __init__(self, minute: str, second: str):
        super().__init__()
        self.minute = minute
        self.second = second

        self.bgcolor = ft.Colors.BLUE_400
        self.padding = ft.padding.all(6)
        self.border_radius = ft.border_radius.all(12)
        self.content = ft.Text(
            f'持续时间：{self.minute}分{self.second}秒',
            size=12,
            color=ft.Colors.BLACK
        )


class NoteCard(ft.Container):
    def __init__(self, note: str | None = None):
        super().__init__()
        self.note = note

        self.bgcolor = ft.Colors.GREY_400
        self.padding = ft.padding.all(6)
        self.border_radius = ft.border_radius.all(12)
        self.content = ft.Text(
            f'备注：{self.note}',
            size=12,
            color=ft.Colors.BLACK
        ) if self.note else None


class HistoryCard(ft.Container):
    def __init__(self, date_time: str, minute: str, second: str, note: str | None = None, delete_callback: Callable[[HistoryCard], None] = None, save_callback: Callable[[], None] = None):
        super().__init__()
        self.date_time = date_time
        self.year = self.tmp_year = self.date_time.split('-')[0]
        self.month = self.tmp_month = self.date_time.split('-')[1]
        self.day = self.tmp_day = self.date_time.split('-')[2].split(' ')[0]
        self.hour = self.tmp_hour = self.date_time.split(' ')[1].split(':')[0]
        self.minute = self.tmp_minute = self.date_time.split(' ')[1].split(':')[1]
        self.second = self.tmp_second = self.date_time.split(' ')[1].split(':')[2]
        self.minute_duration = self.tmp_minute_duration = minute
        self.second_duration = self.tmp_second_duration = second
        self.note = self.tmp_note = note
        self.delete_callback = delete_callback
        self.save_callback = save_callback

        self.date_time_text = ft.Text(self.date_time, size=14, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD)
        self.time_card = TimeCard(self.minute_duration, self.second_duration)
        self.note_card = NoteCard(self.note)

        self.content = ft.Row(
            [
                ft.Column(
                    [
                        self.date_time_text,
                        ft.Row([self.time_card, self.note_card])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ),
                ft.Row(
                    [
                        ft.IconButton(icon=ft.Icons.EDIT, on_click=self.edit),
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=self.delete)
                    ],
                    spacing=-2
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=400,
            height=60
        )
        self.padding = ft.padding.all(12)
        self.border_radius = ft.border_radius.all(16)
        self.bgcolor = ft.Colors.WHITE,
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_GREY_200),
            offset=ft.Offset(1, 1)
        )

        self.edit_dlg = ft.AlertDialog(
            modal=True,
            title='编辑记录',
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.TextField(label='年', width=65, value=self.year, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_year')),
                            ft.Text('-'),
                            ft.TextField(label='月', width=50, value=self.month, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_month')),
                            ft.Text('-'),
                            ft.TextField(label='日', width=50, value=self.day, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_day')),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.TextField(label='时', width=50, value=self.hour, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_hour')),
                            ft.Text(':'),
                            ft.TextField(label='分', width=50, value=self.minute, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_minute')),
                            ft.Text(':'),
                            ft.TextField(label='秒', width=50, value=self.second, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_second')),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Text('持续时间：', size=18),
                            ft.TextField(label='分', width=45, value=str(self.minute_duration), keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_minute_duration')),
                            ft.TextField(label='秒', width=45, value=str(self.second_duration), keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_second_duration'))
                        ]
                    ),
                    ft.TextField(label='备注', width=230, value=self.note, on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_note'))
                ],
                height=222
            ),
            actions=[
                ft.TextButton("保存", on_click=self.save_change),
                ft.TextButton("取消", on_click=lambda e: self.page.close(self.edit_dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: self.page.close(self.edit_dlg)
        )

    def on_edit_dlg_change(self, e, name: str):
        new_value = e.control.value
        setattr(self, name, new_value)

    def _update(self):
        self.date_time_text.value = self.date_time
        self.time_card.content.value = f'持续时间：{self.minute}分{self.second}秒'
        self.note_card.content.value = f'备注：{self.note}'

    def save_change(self, e):
        self.year = self.tmp_year
        self.month = self.tmp_month
        self.day = self.tmp_day
        self.hour = self.tmp_hour
        self.minute = self.tmp_minute
        self.second = self.tmp_second
        self.minute_duration = self.tmp_minute_duration
        self.second_duration = self.tmp_second_duration
        self.note = self.tmp_note
        self.date_time = f'{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}'
        print(self.date_time)
        self._update()
        self.save_callback()
        self.update()
        self.page.close(self.edit_dlg)

    def edit(self, e):
        self.page.open(self.edit_dlg)

    def delete(self, e):
        self.delete_callback(self)


class HistoryPage(ft.Column, Observable):
    def __init__(self):
        super().__init__()
        Observable.__init__(self)
        self.work_dir = Path.cwd()
        self.history_file = self.work_dir / 'history.csv'
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                self.header = next(reader)
                self.history_cards = [
                    HistoryCard(*row, self.delete, self.save) for row in reader
                ]
        except FileNotFoundError:
            self.header = ['date_time', 'minute', 'second', 'note']
            self.history_cards = []
            self.save()

        self.expand = True
        self.alignment = ft.MainAxisAlignment.START
        self.spacing = 10
        self.width = 440
        self.scroll = ft.ScrollMode.HIDDEN
        self.controls = [
            ft.Row(
                [
                    ft.Text('历史记录', size=28, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icons.CLEANING_SERVICES, on_click=self.delete_all)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            *self.history_cards
        ]
        self.file_picker = ft.FilePicker(on_result=self.on_file_picker_result)

    def save(self, path: Path | str | None = None):
        with open(path or self.history_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            for card in self.history_cards:
                writer.writerow([card.date_time, card.minute, card.second, card.note])

    def add(self, card: HistoryCard = None, data: list[str | None] = None):
        if data:
            card = HistoryCard(*data, self.delete, self.save)
        self.history_cards.insert(0, card)
        self.controls.insert(1, card)
        self.save()
        self.notify_callbacks()

    def delete(self, card: HistoryCard):
        self.history_cards.remove(card)
        self.controls.remove(card)
        self.save()
        self.update()
        self.notify_callbacks()

    def delete_all(self, e):
        self.history_cards = []
        self.controls = self.controls[:1]
        self.save()
        self.update()
        self.notify_callbacks()

    def export_csv(self, e):
        self.file_picker.save_file(
            dialog_title="选择导出路径",
            file_name='history.csv',
            allowed_extensions=['csv']
        )

    def import_csv(self, e):
        self.file_picker.pick_files(
            dialog_title="选择导入文件",
            allowed_extensions=['csv'],
            allow_multiple=False
        )

    def on_file_picker_result(self, e: ft.FilePickerResultEvent):
        """ 处理文件选择器结果的回调 """
        if e.path:
            self.export_history_to_path(Path(e.path))
        elif e.files and e.files[0]:
            self.import_history_from_path(Path(e.files[0].path))
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("操作已取消。"), duration=2000, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.SECONDARY))
            self.page.open(self.page.snack_bar)
            self.page.update()

    def export_history_to_path(self, save_path: Path):
        """ 实际的导出逻辑 """
        try:
            with open(save_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)
                writer.writerows([
                    [card.date_time, card.minute, card.second, card.note]
                    for card in self.history_cards
                ])

            self.page.snack_bar = ft.SnackBar(ft.Text(f"导出成功！路径: {save_path}"), duration=2000, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.PRIMARY))

        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"导出失败: {ex}"), duration=2000, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.ERROR))
        finally:
            self.page.open(self.page.snack_bar)
            self.page.update()

    def import_history_from_path(self, file_path: Path):
        """ 实际的导入逻辑 """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                if header != self.header:
                    raise ValueError("文件格式不正确，标题不匹配。")

                i = 0
                for row in reader:
                    card = HistoryCard(*row, self.delete, self.save)
                    self.history_cards.append(card)
                    self.controls.append(card)
                    i += 1

                self.save()
                self.update()
                self.notify_callbacks()

                self.page.snack_bar = ft.SnackBar(ft.Text(f"成功导入 {i} 条记录。"), duration=2000, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.PRIMARY))

        except FileNotFoundError:
            self.page.snack_bar = ft.SnackBar(ft.Text("文件未找到。"), duration=2000, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.ERROR))
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"导入失败: {ex}"), duration=2000, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.ERROR))
        finally:
            self.page.open(self.page.snack_bar)
            self.page.update()
