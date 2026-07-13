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

@ft.control
class UploadDrop(ft.Dropdown):
    
    def init(self):
        self.opt_color = th.ENC_BG
        self.text_size = th.DROP_TEXT
        self.margin = th.SERVER_MRG
        self.value: str = "Servidor SFTP"
        self.color: str = th.ENC_BG
        

        self.trailing_icon = ft.Icon(
            icon=ft.Icons.ARROW_DROP_DOWN, 
            color=th.ENC_BG,
            size=20
        )
        
        self.fill_color = th.ENC_COL 
        self.filled = True
        self.hover_color = th.DROP_HVR
        self.bgcolor = th.ENC_COL 

        self.expand = True
        self.text_align = ft.TextAlign.CENTER
        self.text_size = th.AAA_TEXT
        
        self.text_style = ft.TextStyle(
            weight=ft.FontWeight.BOLD,
            size=th.AAA_TEXT
        )

        self.options: list[ft.DropdownOption] = [
            ft.DropdownOption(
                key="Servidor SFTP",
                content=ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.LOCK, color=self.opt_color),
                        ft.Text(value="Servidor SFTP", color=self.opt_color, weight=ft.FontWeight.BOLD, size=th.DROP_TEXT)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            ft.DropdownOption(
                key="Google Drive",
                content=ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.LOCK_OPEN_SHARP, color=self.opt_color),
                        ft.Text(value="Google Drive", color=self.opt_color, weight=ft.FontWeight.BOLD, size=th.DROP_TEXT)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            )
        ]

    def set_drop_action(self, action):
        self.on_text_change = action

    def set_theme(self, mode):
        if not mode:
            self.opt_color = th.DES_BG
            self.color: str = th.DES_BG
            self.fill_color = th.DES_COL
            self.hover_color = th.DROP_HVR
            self.bgcolor = th.DES_COL
            for option in self.options:
                for control in option.content.controls:
                    control.color = th.DES_BG
