import flet as ft
from .. import themes as th
from .dropdown import AAADropdown

@ft.control
class AAAHeader(ft.Card):
    def init(self):
        self.bgcolor = th.AAA_BG2
        self.margin= th.HEADER_MRG
        self.content= self._create_content()

    def set_drop_action(self, action):
        self.drop.set_drop_action(action)

    def _create_content(self):
        title = ft.Text(
                    spans=[
                        ft.TextSpan("AAA", style=ft.TextStyle(
                                                size=th.AAA_TITLES,
                                                weight=ft.FontWeight.BOLD,
                                                color=th.AAA_COL
                                         )
                        ),
                        ft.TextSpan("  |  ", style=ft.TextStyle(
                                                size=th.AAA_TITLES,
                                                weight=ft.FontWeight.BOLD,
                                                color=th.AAA_COL
                                            )
                        ),
                        ft.TextSpan("Another AES Aplication", style=ft.TextStyle(
                                                                size=th.AAA_SUBTITLES,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=th.AAA_COL
                                                            )
                        )
                    ],
                    expand = 1)
        self.drop = AAADropdown()
        return ft.Row(
                        margin = th.HEADER_MRG,
                        alignment= ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[title, self.drop]
                    )
