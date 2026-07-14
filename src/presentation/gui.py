import flet as ft
from . import themes as th
from .components.header import AAAHeader
from .components.body import AAABody
from .components.buttons import *
        
@ft.control
class AAAWindow(ft.Container):
    def init(self):
        self.border_radius = 10
        self.bgcolor = th.AAA_BG2
        self.color = th.AAA_COL
        self.expand = True
        self.margin = 5
        self.body = self._build_body()
        self.change_state = self.body.change_state
        self.header = self._build_header()
        self.content = ft.Column(
            alignment= ft.MainAxisAlignment.START,
            horizontal_alignment= ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.header,
                self.body
            ]
            )

    def _build_header(self):
        self.header = AAAHeader()
        self.header.set_drop_action(self.change_state)
        return self.header
    
    def _build_body(self):
        return AAABody()

async def main(page: ft.Page):
    page.title = "AAA"
    page.bgcolor = th.AAA_BG
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    await page.window.center()
    page.add(AAAWindow())

def AAAStart():
    ft.run(main)
