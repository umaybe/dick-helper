import time
import threading
from datetime import datetime
from functools import cached_property

import flet as ft

from history import HistoryPage


class TimerCard(ft.Card):
    """A simple timer card """

    def __init__(self, history_manager: HistoryPage):
        super().__init__()
        self.history_manager = history_manager
        self.is_running = False
        self.is_paused = False
        self.elapsed_time = 0
        self.last_tick_time = 0
        self.running = True  # Control the background thread
        # Start the background thread
        self.thread = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.thread.start()

        # Static controls
        self.title_text = ft.Text(
            "记录新的手艺活",
            size=16,
            color=ft.Colors.BLUE_600,
            weight=ft.FontWeight.BOLD
        )
        self.status_text = ft.Text(
            value="准备开始",
            size=40,
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER
        )
        self.dynamic_controls_container = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=self.build_stopped_view()
        )
        self.notes_field = ft.TextField(
            hint_text="备注 (可选)",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True
        )
        self.export_button = ft.TextButton(
            "导出数据",
            icon=ft.Icons.DOWNLOAD,
            on_click=self.history_manager.export_csv
        )
        self.import_button = ft.TextButton(
            "导入数据",
            icon=ft.Icons.UPLOAD,
            on_click=self.history_manager.import_csv
        )

        self.elevation = 4.0,
        self.content = ft.Container(
            width=350,
            padding=ft.padding.all(20),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    self.title_text,
                    self.dynamic_controls_container,  # Dynamic area
                    ft.Row(controls=[self.notes_field]),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[self.export_button, self.import_button],
                    )
                ]
            )
        )

    def update_timer(self):
        """Background thread function to update the timer every second."""
        while self.running:
            if self.is_running and not self.is_paused:
                now = time.time()
                self.elapsed_time += now - self.last_tick_time
                self.last_tick_time = now

                # Update UI
                mins, secs = divmod(int(self.elapsed_time), 60)
                self.status_text.value = f"{mins}分{secs}秒"
                if self.status_text.page:  # Ensure the page is available
                    self.status_text.update()

            time.sleep(0.5)  # Check status every 0.5 seconds for responsive pause/resume

    def start_clicked(self, e):
        """Handle 'Start' button click event."""
        self.is_running = True
        self.is_paused = False
        self.elapsed_time = 0
        self.last_tick_time = time.time()
        self.switch_to_running_view()

    def end_clicked(self, e):
        """Handle 'End' button click event."""
        self.is_running = False
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mins, self.secs = divmod(int(self.elapsed_time), 60)
        self.note = self.notes_field.value
        self.history_manager.add(
            data=[now, self.mins, self.secs, self.note]
        )
        self.elapsed_time = 0
        self.switch_to_stopped_view()

    def pause_clicked(self, e):
        """Handle 'Pause/Resume' button click event."""
        self.is_paused = not self.is_paused
        if not self.is_paused:
            # Reset the timing start point for resume
            self.last_tick_time = time.time()

        # Update button text and icon
        self.pause_button.text = "继续" if self.is_paused else "暂停"
        self.pause_button.icon = ft.Icons.PLAY_ARROW_ROUNDED if self.is_paused else ft.Icons.PAUSE_ROUNDED
        if self.pause_button.page:  # Ensure the page is available
            self.pause_button.update()

    def build_stopped_view(self):
        """Build the UI elements for the stopped state."""
        self.status_text.value = "准备开始"
        self.status_text.size = 40

        start_button = ft.ElevatedButton(
            text="开始",
            icon=ft.Icons.PLAY_ARROW,
            height=50,
            width=100,
            style=ft.ButtonStyle(
                shape=ft.StadiumBorder(),
                bgcolor=ft.Colors.BLUE_400,
                color=ft.Colors.WHITE,
            ),
            on_click=self.start_clicked,
        )
        return [self.status_text, start_button]

    def build_running_view(self):
        """Build the UI elements for the running state."""
        self.status_text.value = "0分0秒"
        self.status_text.size = 48  # Larger font for running state

        self.end_button = ft.FilledButton(
            text="结束",
            icon=ft.Icons.STOP_ROUNDED,
            height=50,
            width=100,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED),
                color=ft.Colors.RED_600,
            ),
            on_click=self.end_clicked
        )
        self.pause_button = ft.FilledButton(
            text="暂停",
            icon=ft.Icons.PAUSE_ROUNDED,
            height=50,
            width=100,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                bgcolor=ft.Colors.ORANGE_400,
                color=ft.Colors.WHITE,
            ),
            on_click=self.pause_clicked,
        )

        button_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[self.end_button, self.pause_button]
        )
        return [self.status_text, button_row]

    def switch_to_stopped_view(self):
        """Switch UI to stopped view."""
        self.dynamic_controls_container.controls = self.build_stopped_view()
        if self.dynamic_controls_container.page:  # Ensure the page is available
            self.dynamic_controls_container.update()

    def switch_to_running_view(self):
        """Switch UI to running view."""
        self.dynamic_controls_container.controls = self.build_running_view()
        if self.dynamic_controls_container.page:  # Ensure the page is available
            self.dynamic_controls_container.update()

    def cleanup(self):
        """Stop the background thread when the app closes."""
        self.running = False


def create_card(title: str, value: str, unit: str = ""):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    title,
                    size=14,
                ),
                ft.Row(
                    [
                        # 使用Container和Text的组合使不同字号的Text能够看起来下端对齐
                        ft.Column(
                            [
                                ft.Container(height=0),
                                ft.Text(
                                    value,
                                    size=36,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE
                                ),
                            ],
                            spacing=0,
                            alignment=ft.MainAxisAlignment.START
                        ),
                        ft.Column(
                            [
                                ft.Container(height=20),
                                ft.Text(
                                    unit,
                                    size=12
                                )
                            ],
                            spacing=0,
                            alignment=ft.MainAxisAlignment.START
                        ),
                    ],
                    spacing=2
                )
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.padding.all(15),
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(1, 1),
        )
    )


class StatsView(ft.Container):
    def __init__(self, history_manager: HistoryPage):
        super().__init__()
        self.history_manager = history_manager
        self.history_manager.register_callback(self._update)

        self.grid = ft.GridView(
            expand=True,
            max_extent=160,
            runs_count=4,
            child_aspect_ratio=1.6,
            spacing=15,
            run_spacing=15,
            controls=[
                create_card("总次数", str(self.total_times)),
                create_card("平均持续时间", str(self.avg_minute), "分钟"),
                create_card("本周次数", str(self.this_week_times)),
                create_card("本月次数", str(self.this_month_times)),
            ]
        )
        self.content = ft.Column(
            [
                ft.Text(
                    "统计数据",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE
                ),
                self.grid
            ],
            spacing=20
        )
        self.padding = ft.padding.all(20)

    @property
    def total_times(self):
        return self.history_manager.history_cards.__len__()

    @cached_property
    def _time_stats(self):
        _minute = _second = 0
        for card in self.history_manager.history_cards:
            _minute += int(card.minute)
            _second += int(card.second)
        return _minute, _second

    @property
    def minute(self):
        return self._time_stats[0]

    @property
    def second(self):
        return self._time_stats[1]

    @property
    def avg_minute(self):
        return round((self.minute + self.second / 60) / self.total_times, 2)

    @cached_property
    def _duration_stats(self):
        _this_month_times = _this_week_times = 0
        for card in self.history_manager.history_cards:
            _date = card.date_time.split(' ')[0]
            _date = datetime.strptime(_date, "%Y-%m-%d").date()
            if _date.year == datetime.now().year and _date.month == datetime.now().month:
                _this_month_times += 1
            if _date.isocalendar().week == datetime.now().isocalendar().week:
                _this_week_times += 1
        return _this_month_times, _this_week_times

    @property
    def this_month_times(self):
        return self._duration_stats[0]

    @property
    def this_week_times(self):
        return self._duration_stats[1]

    def clear_time_stats_cache(self):
        """ 清除缓存，当下次访问时会重新计算 """
        if hasattr(self, '_time_stats'):
            del self._time_stats
        if hasattr(self, '_duration_stats'):
            del self._duration_stats

    def _update(self):
        self.clear_time_stats_cache()
        if self.page:  # Ensure the page is available
            self.grid.controls = [
                create_card("总次数", str(self.total_times)),
                create_card("平均持续时间", str(self.avg_minute), "分钟"),
                create_card("本周次数", str(self.this_week_times)),
                create_card("本月次数", str(self.this_month_times)),
            ]
            self.update()


class HomePage(ft.Column):
    def __init__(self, history_manager: HistoryPage):
        super().__init__()
        self.history_manager = history_manager

        self.controls = [
            ft.Row(
                [
                    ft.Text("主页", size=28, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icons.ADD, on_click=lambda e: self.page.open(self.add_dlg))
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            TimerCard(self.history_manager),
            ft.Divider(),
            StatsView(self.history_manager)
        ]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.START
        self.spacing = 10
        self.scroll = ft.ScrollMode.HIDDEN

        self.add_dlg = ft.AlertDialog(
            modal=True,
            title='添加记录',
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.TextField(label='年', width=65, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_year')),
                            ft.Text('-'),
                            ft.TextField(label='月', width=50, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_month')),
                            ft.Text('-'),
                            ft.TextField(label='日', width=50, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_day')),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.TextField(label='时', width=50, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_hour')),
                            ft.Text(':'),
                            ft.TextField(label='分', width=50, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_minute')),
                            ft.Text(':'),
                            ft.TextField(label='秒', width=50, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_second')),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Text('持续时间：', size=18),
                            ft.TextField(label='分', width=45, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_minute_duration')),
                            ft.TextField(label='秒', width=45, keyboard_type=ft.KeyboardType.NUMBER,
                                         on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_second_duration'))
                        ]
                    ),
                    ft.TextField(label='备注', width=230, on_change=lambda e: self.on_edit_dlg_change(e, 'tmp_note'))
                ],
                height=222
            ),
            actions=[
                ft.TextButton("保存", on_click=self.save_change),
                ft.TextButton("取消", on_click=lambda e: self.page.close(self.add_dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: self.page.close(self.add_dlg)
        )

    def on_edit_dlg_change(self, e, name: str):
        new_value = e.control.value
        setattr(self, name, new_value)

    def save_change(self, e):
        self.date_time = f'{self.tmp_year}-{self.tmp_month}-{self.tmp_day} {self.tmp_hour}:{self.tmp_minute}:{self.tmp_second}'
        self.minute_duration = int(self.tmp_minute_duration)
        self.second_duration = int(self.tmp_second_duration)
        self.note = self.tmp_note
        to_add = [self.date_time, self.minute_duration, self.second_duration, self.note]
        self.history_manager.add(data=to_add)
        self.page.close(self.add_dlg)
