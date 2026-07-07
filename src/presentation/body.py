from dataclasses import dataclass
import flet as ft
import themes as th

@dataclass
class FileInfo:
    name: str = ""
    weight: str = ""
    date: str = ""
    path: str = ""
    extension: str = ""
    bytes: str = ""

@ft.control
class LeftColumnContent(ft.Container):
    
    def init(self):
        self.border = ft.Border.all(width=2, color=th.AAA_COL)
        self.border_radius = ft.BorderRadius.all(5)
        self.padding = 10
        self.expand = True
        
        self.scrollable = ft.ListView(
            expand=True,
            spacing=12,
        )
        self.content = self.scrollable
        
        self.clear_data()

    def clear_data(self):
        """Muestra los campos vacíos o por defecto"""
        vacio = FileInfo()
        self.update_data(vacio)

    def update_data(self, new_file_info: FileInfo):
        """¡El método mágico dinámico! Llámalo cada vez que el archivo cambie"""
        
        fields_to_render = [
            ("Nombre:", new_file_info.name),
            ("Peso:", new_file_info.weight),
            ("Fecha:", new_file_info.date),
            ("Ruta:", new_file_info.path),
            ("Extensión:", new_file_info.extension),
            ("Bytes:", new_file_info.bytes),
        ]
        
        self.scrollable.controls.clear()

        for label, value in fields_to_render:
            self.scrollable.controls.append(
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            text=f"{label} ",
                            style=ft.TextStyle(
                                weight=ft.FontWeight.BOLD,
                                color=th.AAA_COL,
                                size=th.AAA_TEXT
                            )
                        ),
                        ft.TextSpan(
                            text=str(value),
                            style=ft.TextStyle(
                                weight=ft.FontWeight.NORMAL,
                                color=th.AAA_COL,
                                size=th.AAA_DROP
                            )
                        )
                    ]
                )
            )

@ft.control
class AAABody(ft.Card):
    def init(self):
        self.state:bool = True #Encrypt o Decrypt
        self.expand = 1
        self.bgcolor = th.BODY_BG
        self.margin = th.BODY_MRG
        self.shadow_color = ft.Colors.ON_SURFACE_VARIANT
        
        self.content = Encrypt()

@ft.control
class Encrypt(ft.Container):
    def init(self):
        self.margin = th.BODY_MRG
        #self.bgcolor = 'red'
        
        self.left_column = self._build_left_column()
        self.content = ft.Row(
            controls = [
                self.left_column,
                ft.Column(expand=1)
            ])
    
    def _build_left_column(self):
        self.name = ""
        self.weight = ""
        self.date = ""
        self.path = ""
        self.extension = ""
        self.bytes = ""

        self.file_state = False
        self.title_icon = ft.Icons.FILE_OPEN#ft.Icons.FILE_DOWNLOAD_DONE
        self.title = ft.Container(
                            content = ft.Row(
                                controls= [
                                    ft.Text('Archivo Plano',
                                    size= th.AAA_TEXT,
                                    color= th.AAA_COL,
                                    weight=ft.FontWeight.BOLD
                                    ),
                                    ft.IconButton(icon = self.title_icon, icon_color=th.AAA_COL, hover_color=th.BODY_BUT_COL)]
                                )
                            )
        
        
        
        self.lcol_content = LeftColumnContent()
        return ft.Column(
            margin = th.ENC_MRG,
            expand=1,
            controls= [
                self.title,
                self.lcol_content
                ])
