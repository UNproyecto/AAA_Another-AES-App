from dataclasses import field
import flet as ft
from .. import themes as th
from .dropdown import UploadDrop
from domain import models as md
from domain import AAA

@ft.control
class MainDialog (ft.AlertDialog):
    title : ft.Text = field( default_factory=lambda: ft.Text("Por favor ingrese la información requerida"))
    content : ft.Text = ft.Text("Please sign in again to continue.")
    actions : list[ft.TextButton] = field( default_factory=lambda: [ft.TextButton("Dismiss")] )
    open : bool = True

@ft.control
class PwdContent(ft.Column):
    
    def init(self):
        self.margin = th.DIAL_MRG
        self.tight = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.pwd = ft.TextField(
                            label="Contraseña de encriptación",
                            tooltip="Contraseña de encriptación",
                            border_color=th.ENC_COL,
                            prefix_icon = ft.Icons.LOCK_OUTLINE)
        self.path = ft.TextField(
                            label="Ruta",
                            tooltip="Ruta o Path al archivo",
                            border_color=th.ENC_COL,
                            prefix_icon = ft.Icons.ROUTE)
        self.controls = [self.pwd, self.path]
    
    def rem_path(self):
        self.path.visible = False

    def get_pwd(self):
        return self.pwd.value
    
    def get_path(self):
        return self.path.value

    def reset_content(self):
        self.pwd.value = ''
        self.path.value = ''

    def set_theme(self, mode):
        if not mode :
            self.color = th.DES_COL
            for control in self.controls:
                control.border_color = th.DES_COL
                control.color = th.DES_COL
                control.label_style = ft.TextStyle(
                                        color=th.DES_COL
                )
                control.prefix_icon.color = th.DES_COL

@ft.control
class EncrDialog(MainDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent_component = parent
    def init(self):
        self.title.color = th.ENC_COL
        self.bgcolor = th.ENC_BG
        self.cont = PwdContent()
        self.cont.rem_path()
        self.content = ft.Card(
            bgcolor = th.ENC_DIAL_BG,
            content = self.cont
        )
        self.button = ft.TextButton(content = "Encriptar", on_click=self.encrypt)
        self.actions = [self.button] 
    
    def reset_dialog(self):
        self.cont.reset_content()
    
    def get_pwd(self):
        return self.cont.get_pwd()

    def encrypt(self):
        file = self.parent_component.file
        if file is not None:
            metadata = {
                'name' : file.name,
                'weight' : file.weight,
                'path' : file.path,
                'extension' : file.extension
            }
            file = file.bytes
            file = md.Archivo(metadata= metadata, contenido = file)
            encr_file = AAA.encrypt(pwd= self.get_pwd(),
                        archivo= file)

            self.parent_component.set_encrypted(encr_file)
            self.page.pop_dialog()
        


    

@ft.control
class ConnectionCard(ft.Card):
    def init(self):
        self.drop = UploadDrop()
        self.server_form = ServerForm()
        self.content = ft.Row(
                            controls=[
                                    self.drop,
                                    self.server_form
                                    ])
    
    def set_theme(self, mode):
        if mode is False:
            self.bgcolor = th.DES_DIAL_BG
            self.server_form.set_theme(False)
        else:
            self.bgcolor = th.ENC_DIAL_BG
            self.server_form.set_theme(True)
    
    def reset_card(self):
        self.server_form.reset_content()
        


@ft.control
class ServerForm(ft.Column):
    def init(self):
        self.tight = True
        self.margin = th.SERVER_MRG
        self.border_color =  th.ENC_COL
        self.text_color = th.ENC_COL
        self.ip = ft.TextField(
                            label="IP",
                            tooltip="Dirección IP del servidor SMTP",
                            border_color=self.border_color,
                            prefix_icon = ft.Icon(
                                                icon=ft.Icons.WIFI, 
                                                color=self.text_color,
                                                size=20
                                            ))
        self.usr = ft.TextField(
                            label="Usuario",
                            tooltip="Usuario activo en servidor SMTP",
                            border_color=self.border_color,
                            prefix_icon = ft.Icon(
                                                icon=ft.Icons.PERSON, 
                                                color=self.text_color,
                                                size=20
                                            ))
        
        self.pwd = ft.TextField(
                            label="Contraseña",
                            tooltip="Contraseña de ervidor SMTP",
                            border_color=self.border_color,
                            prefix_icon = ft.Icon(
                                                icon=ft.Icons.LOCK_OUTLINE, 
                                                color=self.text_color,
                                                size=20
                                            ))
        
        self.controls = [self.ip, self.usr, self.pwd]

    def reset_content(self):
        self.ip.value = ''
        self.usr.value = ''
        self.pwd.value = ''

    def set_theme(self, mode):
        if not mode :
            self.color = th.DES_COL
            for control in self.controls:
                control.border_color = th.DES_COL
                control.color = th.DES_COL
                control.label_style = ft.TextStyle(
                                        color=th.DES_COL
                )
                control.prefix_icon.color = th.DES_COL

@ft.control
class PathCard(ft.Card):
    def init(self):
        self.expand = True
        self.bgcolor = th.ENC_DIAL_BG
        self.content = ft.TextField(
                                    margin = th.SERVER_MRG,
                                    label="Ruta de guardado",
                                    tooltip="Ruta en la que el archivo será guardado",
                                    border_color=th.ENC_COL,
                                    prefix_icon = ft.Icon(
                                                icon=ft.Icons.ROUTE, 
                                                color=th.ENC_COL,
                                                size=20
                                            ))
    def set_theme(self, mode):
        if not mode:
            self.bgcolor = th.DES_DIAL_BG
            self.content.prefix_icon.color = th.DES_COL
            self.color = th.DES_COL
            self.content.color = th.DES_COL
            self.content.border_color = th.DES_COL
            self.content.label_style = ft.TextStyle(
                                        color=th.DES_COL
                )
    
    def reset_content(self):
        self.content.value = ''

@ft.control
class CloudUploadDialog(MainDialog):
    def init(self):
        self.title.color = th.ENC_COL
        self.connected = False
        self.bgcolor = th.ENC_BG
        self.card = ConnectionCard()
        self.file_location = PathCard()
        self.card.set_theme(True)
        self.content = ft.Column(
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                tight= True,
                                controls = [
                                    self.card,
                                    ft.Row(self.file_location)
                                    ]
                                )
        self.conect = ft.TextButton("Conectar", icon=ft.Icons.WIFI)
        self.upload = ft.TextButton("Subir", icon=ft.Icons.UPLOAD)
        self.actions = [self.conect, self.upload] 

    def reset_dialog(self):
        self.card.reset_card()
        self.file_location.reset_content()

@ft.control
class CloudDownloadDialog(MainDialog):
    def init(self):
        self.title.color = th.DES_COL
        self.connected = False
        self.bgcolor = th.DES_BG
        self.card = ConnectionCard()
        self.file_location = PathCard()
        self.file_location.set_theme(False)
        self.card.set_theme(False)
        self.card.drop.set_theme(False)
        self.content = ft.Column(
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                tight= True,
                                controls = [
                                    self.card,
                                    ft.Row(self.file_location)
                                    ]
                                )
        self.conect = ft.TextButton("Conectar", icon=ft.Icon(
                                                    icon=ft.Icons.WIFI,
                                                    color=th.DES_COL,
                                                    size=20,
                                                    ),
                                                    style=ft.ButtonStyle(
                                                        color=th.DES_COL,
                                                    ),
                                    )

        self.upload = ft.TextButton("Bajar",icon=ft.Icon(
                                                    icon=ft.Icons.DOWNLOAD,
                                                    color=th.DES_COL,
                                                    size=20,
                                                ),
            
                                            style=ft.ButtonStyle(
                                                color=th.DES_COL,
                                            ),
                                        )
        self.actions = [self.conect, self.upload] 
    
    def reset_dialog(self):
        self.card.reset_card()
        self.file_location.reset_content()

@ft.control
class LocalDownloadDialog(MainDialog):
    def init(self):
        self.title.color = th.DES_COL
        self.bgcolor = th.DES_BG
        self.cont = PwdContent()
        self.cont.set_theme(False)
        self.content = ft.Card(
            bgcolor = th.DES_DIAL_BG,
            content = self.cont
        )
        self.button = ft.TextButton("Desencriptar y Guardar",icon=ft.Icon(
                                                    icon=ft.Icons.DOWNLOAD,
                                                    color=th.DES_COL,
                                                    size=20,
                                                ),
            
                                            style=ft.ButtonStyle(
                                                color=th.DES_COL,
                                            ),)
        self.actions = [self.button] 
    
    def reset_dialog(self):
        self.cont.reset_content()
    