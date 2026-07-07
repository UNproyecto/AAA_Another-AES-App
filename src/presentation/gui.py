from dataclasses import field
import flet as ft
import themes as th
from header import AAAHeader
from body import AAABody

@ft.control
class AAAButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)

@ft.control
class EncryptButton(AAAButton):
    bgcolor: str = th.ENC_BG
    color: str = th.ENC_COL


@ft.control
class DecryptButton(AAAButton):
    bgcolor: str = th.DES_BG
    color: str = th.DES_COL

        
@ft.control
class AAAWindow(ft.Container):
    def init(self):
        self.border_radius = 10
        self.bgcolor = th.AAA_BG2
        self.color = th.AAA_COL
        self.expand = True
        self.margin = 5
        self.header = self._build_header()
        self.body = self._build_body()
        self.content = ft.Column(
            alignment= ft.MainAxisAlignment.START,
            horizontal_alignment= ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.header,
                self.body
            ]
            )

    def _build_header(self):
        return AAAHeader()
    
    def _build_body(self):
        return ft.Row(expand= True,
                      controls=[AAABody()])
    
        

async def main(page: ft.Page):
    page.title = "AAA"
    page.bgcolor = th.AAA_BG
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    await page.window.center()
    
    page.add(AAAWindow())
        



ft.run(main)
