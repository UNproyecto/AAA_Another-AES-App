import flet as ft
import themes as th
@ft.control
class AAADropdown(ft.Dropdown):
    
    def init(self):
        self.value: str = "Encriptar"
        self.color: str = th.AAA_COL
        self.bgcolor = th.DROP_BG
        self.fill_color = th.DROP_BG
        self.filled = True
        self.trailing_icon = ft.Icon(
            icon=ft.Icons.ARROW_DROP_DOWN, 
            color=th.AAA_COL,
            size=30
        )
        

        self.hover_color = th.DROP_HVR

        self.text_align = ft.TextAlign.CENTER
        self.text_size = th.AAA_DROP
        self.expand = 1
        
        self.text_style = ft.TextStyle(
            weight=ft.FontWeight.BOLD,
            size=th.AAA_DROP
        )

        self.options: list[ft.DropdownOption] = [
            ft.DropdownOption(
                key="Encriptar",
                content=ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.LOCK, color=th.AAA_COL),
                        ft.Text(value="Encriptar", color=th.AAA_COL, weight=ft.FontWeight.BOLD, size=th.AAA_OPTIONS)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            ft.DropdownOption(
                key="Desencriptar",
                content=ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.LOCK_OPEN_SHARP, color=th.AAA_COL),
                        ft.Text(value="Desencriptar", color=th.AAA_COL, weight=ft.FontWeight.BOLD, size=th.AAA_OPTIONS)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            )
        ]

    def set_drop_action(self, action):
        self.on_text_change = action