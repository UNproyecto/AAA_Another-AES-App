from dataclasses import dataclass
import flet as ft
import themes as th
from .buttons import *


@dataclass
class FileInfo:
    name: str = ""
    weight: str = ""
    path: str = ""
    extension: str = ""
    bytes: str = ""

@ft.control
class LeftColumnContent(ft.Column):
    
    def init(self):
        self.state = 0
        self.title_options = ['Archivo Encriptado', 'Archivo Plano']
        self.expand = 1
        self.margin = th.BODY_MRG
        self.alignment = ft.MainAxisAlignment.START
        self.title_icon = ft.Icons.FILE_OPEN#ft.Icons.FILE_DOWNLOAD_DONE
        self.title = ft.Container(
                        content = ft.Row(
                            controls= [
                                ft.Text('Archivo Encriptado',
                                size= th.AAA_TEXT,
                                color= th.AAA_COL,
                                weight=ft.FontWeight.BOLD
                                ),
                                ft.IconButton(icon = self.title_icon, icon_color=th.AAA_COL, hover_color=th.BODY_BUT_COL)]
                            )
                        )
        
        self.scrollable = ft.ListView(
            height=th.BODY_VIEWS_HEIGHT,
            spacing=5,
        )

        self.scroll_container = ft.Container(
                border = ft.Border.all(width=2, color=th.AAA_COL),
                border_radius = ft.BorderRadius.all(5),
                padding = 10,
                expand = True,
                content=self.scrollable
            )
        self.controls = [
            self.title,
            self.scroll_container
        ]
        
        
        self.clear_data()

    def change_state(self):
        self.state = not self.state
        self.title.content.controls[0].value = self.title_options[self.state]
    
    def clear_data(self):
        """Muestra los campos vacíos o por defecto"""
        vacio = FileInfo()
        self.update_data(vacio)

    def update_data(self, new_file_info: FileInfo):
        
        fields_to_render = [
            ("Nombre:", new_file_info.name),
            ("Peso (bytes):", new_file_info.weight),
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
                                size=th.AAA_TEXT
                            )
                        )
                    ]
                )
            )

@ft.control
class RightColumnContent(ft.Column):
    
    def init(self):
        self.state = 0
        self.title_options = ['Archivo Plano', 'Archivo Encriptado']
        self.expand = 1
        self.margin = th.BODY_MRG
        self.title = ft.Container(
                            content = ft.Row(
                                controls= [
                                    ft.Text('Archivo Plano',
                                    size= th.AAA_LTEXT,
                                    color= th.AAA_COL,
                                    weight=ft.FontWeight.BOLD
                                    ),
                                    ft.IconButton(icon = ft.Icons.KEY, icon_color=th.AAA_COL, hover_color=th.BODY_BUT_COL)]
                                )
                            )
        self.scrollable = ft.ListView(
            height=th.BODY_VIEWS_HEIGHT,
            spacing=5,
        )

        self.scroll_container = ft.Container(
                border = ft.Border.all(width=2, color=th.AAA_COL),
                border_radius = ft.BorderRadius.all(5),
                padding = 10,
                expand = 1,
                content=self.scrollable
                
            )
        self.controls = [
            self.title,
            self.scroll_container
        ]

    def clear_data(self):
        self.scrollable.controls.clear()
        self.scrollable.controls.append(
            ft.Text(
                value='',
                color=th.AAA_COL,
                size=th.AAA_TEXT,
            )
        )
        self.update()

    def write_binary_data(self, binary_text: str, chunk_size: int = 80):
        self.scrollable.controls.clear()
        if not binary_text:
            self.clear_data()
            return

        for i in range(0, len(binary_text), chunk_size):
            chunk = binary_text[i:i + chunk_size]
            self.scrollable.controls.append(
                ft.Text(
                    value=chunk,
                    color=th.AAA_COL,
                    size=th.AAA_TEXT,
                )
            )
        self.update()

    def change_state(self):
        self.state = not self.state
        self.title.content.controls[0].value = self.title_options[self.state]
    
        
@ft.control
class AAABody(ft.Card):
    def init(self):

        self.picker = ft.FilePicker()
        self.state:bool = True #Encrypt o Decrypt
        self.bgcolor = th.BODY_BG
        self.margin = th.BODY_MRG
        self.shadow_color = ft.Colors.ON_SURFACE_VARIANT
        self.expand = 1
        self.left_col = LeftColumnContent()
        self.right_col = RightColumnContent()
        self.info = ft.Row(
                    expand = 2,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                            self.left_col,
                            self.right_col
                        ]
                )
        
        self.enc_select = EncryptButton(
                                        visible = False,
                                        content=
                                        ft.Text('Cargar y Encriptar', size=th.AAA_TEXT,),
                                        icon=ft.Icons.UPLOAD_FILE,
                                        on_click=self.seleccionar
                                        )
        self.enc_encrypt = EncryptButton(
                                        visible = False,
                                        content=
                                        ft.Text('Subir', size=th.AAA_TEXT),
                                        icon=ft.Icons.CLOUD,
                                        on_click=lambda x: None
                                        )
        self.dec_select = DecryptButton(
                                        visible = True,
                                        content=
                                        ft.Text('Recuperar', size=th.AAA_TEXT,),
                                        icon=ft.Icons.CLOUD,
                                        on_click=lambda x: None)
        self.dec_dencrypt = DecryptButton(
                                        visible= True,
                                        content=
                                        ft.Text('Descargar y Desencriptar', size=th.AAA_TEXT),
                                        icon=ft.Icons.DOWNLOAD,
                                        on_click=lambda x: None)
        self.controls = ft.Row(
                            expand=1,
                            margin = th.BODY_MRG,
                            controls=[
                                self.enc_select,
                                self.enc_encrypt,
                                self.dec_select,
                                self.dec_dencrypt
                            ]
                        )
        
        self.content = ft.Column(
            alignment= ft.MainAxisAlignment.CENTER,
            controls = [
                self.info,
                self.controls
                ]
        )
    
    async def seleccionar(self, e):
        raw : list[ft.FilePickerFile] = await self.picker.pick_files(
            allow_multiple= False,
            with_data= True
        )
        if len(raw) > 0:
            raw : ft.FilePickerFile = raw[0]
            extension = self.get_extension(raw.name)
            file = FileInfo(name = raw.name, weight = raw.size, path = raw.path, extension=extension, bytes = raw.bytes)
            self.left_col.update_data(file)
        else:
            pass
        
    def get_extension(self, name:str):
        start = name.index(".")
        return name[start:]
        
    
    def change_state(self):
        self.state = not self.state
        for button in self.controls.controls:
            button.visible = not button.visible
        self.left_col.change_state()
        self.right_col.change_state()
        self.left_col.clear_data()
        self.right_col.clear_data()
        self.update()
