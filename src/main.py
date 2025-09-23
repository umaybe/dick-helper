import flet as ft

from history import HistoryPage
from settings import SettingsPage
from home import HomePage, TimerCard


def main(page: ft.Page):
    page.adaptive = True
    page.title = '牛子小助手'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 375
    page.window.height = 700
    page.window.resizable = False
    page.window.maximizable = False

    history_page = HistoryPage()
    page.overlay.append(history_page.file_picker)
    settings_page = SettingsPage()
    home_page = HomePage(history_page)

    timer_card = None
    for control in home_page.controls:
        if isinstance(control, TimerCard):
            timer_card = control
            break

    page_stack = ft.Stack(controls=[home_page, history_page, settings_page], expand=True)

    def on_nav_change(e: ft.ControlEvent):
        """ Handle navigation bar changes """
        selected_index = e.control.selected_index
        home_page.visible = (selected_index == 0)
        history_page.visible = (selected_index == 1)
        settings_page.visible = (selected_index == 2)
        page.update()

    history_page.visible = False
    settings_page.visible = False

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label='主页'
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.HISTORY_OUTLINED,
                selected_icon=ft.Icons.HISTORY,
                label='历史'
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label='设置'
            )
        ],
        on_change=on_nav_change,
        selected_index=0,
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND)
    )

    page.add(page_stack)
    page.on_close = lambda: timer_card.cleanup()


ft.app(main)
