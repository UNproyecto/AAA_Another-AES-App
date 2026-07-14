from dataclasses import field
import flet as ft
from .. import themes as th
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
