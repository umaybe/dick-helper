import flet as ft


class SettingsPage(ft.Column):
    def __init__(self):
        super().__init__()

        self.theme_group = ft.RadioGroup(
            value="system",
            on_change=self.on_theme_change,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CONTRAST, size=24),
                            ft.Text("跟随系统", size=16),
                            ft.Container(
                                content=ft.Radio(value="system"),
                                expand=True,
                                alignment=ft.alignment.center_right
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=16
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LIGHT_MODE, size=24),
                            ft.Text("浅色模式", size=16),
                            ft.Container(
                                content=ft.Radio(value="light"),
                                expand=True,
                                alignment=ft.alignment.center_right
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=16
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DARK_MODE, size=24),
                            ft.Text("深色模式", size=16),
                            ft.Container(
                                content=ft.Radio(value="dark"),
                                expand=True,
                                alignment=ft.alignment.center_right
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=16
                    )
                ],
                spacing=16
            )
        )

        self.app_details = ft.Column(
            [
                ft.Text("APP 版本:", size=16),
                ft.Text("Flet SDK 版本:", size=16),
                ft.Text("Python 版本:", size=16),
            ],
            spacing=24,
        )
        self.version_values = ft.Column(
            [
                ft.Text("0.1.0", size=16),
                ft.Text("0.28.3", size=16),
                ft.Text("3.13.7", size=16),
            ],
            spacing=24,
        )

        self.controls = [
            ft.Text("设置", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("主题", size=16, weight=ft.FontWeight.NORMAL),
            self.theme_group,
            ft.Divider(),
            ft.Text("应用信息", size=16, weight=ft.FontWeight.NORMAL),
            ft.Row([self.app_details, self.version_values], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ]
        self.padding = 20
        self.spacing = 24
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN

    def on_theme_change(self, e: ft.ControlEvent):
        match e.control.value:
            case 'light':
                self.page.theme_mode = ft.ThemeMode.LIGHT
            case 'dark':
                self.page.theme_mode = ft.ThemeMode.DARK
            case _:
                self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.update()


if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "设置"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window.width = 375
        page.window.height = 700
        page.window.resizable = False
        page.window.maximizable = False
        page.add(SettingsPage())

    ft.app(main)
