import flet as ft
import themes as th
from dropdown import AAADropdown

@ft.control
class AAAHeader(ft.Card):
    def init(self):
        self.bgcolor = th.AAA_BG2
        self.margin= th.HEADER_MRG
        self.content= ft.Row(
                        margin = th.HEADER_MRG,
                        alignment= ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "AAA",
                                            style=ft.TextStyle(
                                                size=th.AAA_TITLES,
                                                weight=ft.FontWeight.BOLD,
                                                color=th.AAA_COL
                                            )
                                        ),
                                        ft.TextSpan(
                                            "  |  ",
                                            style=ft.TextStyle(
                                                size=th.AAA_TITLES,
                                                weight=ft.FontWeight.BOLD,
                                                color=th.AAA_COL
                                            )
                                        ),
                                        ft.TextSpan(
                                            "Another AES Aplication",
                                            style=ft.TextStyle(
                                                size=th.AAA_SUBTITLES,
                                                weight=ft.FontWeight.BOLD,
                                                color=th.AAA_COL
                                            )
                                        )
                                    ],
                                    expand = 1),
                            AAADropdown()
                            ])