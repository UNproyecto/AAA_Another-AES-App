from dataclasses import field
import flet as ft
from .. import themes as th
from .dropdown import UploadDrop
from domain import models as md
from domain import AAA
from adapters import adaptador_sftp as sftp

@ft.control
class MainDialog (ft.AlertDialog):
    title : ft.Text = field( default_factory=lambda: ft.Text("Por favor ingrese la información requerida"))
    content : ft.Text = ft.Text("Please sign in again to continue.")
    actions : list[ft.TextButton] = field( default_factory=lambda: [ft.TextButton("Dismiss")] )
    open : bool = False

@ft.control
class PwdContent(ft.Column):
    
    def init(self):
        self.margin = th.DIAL_MRG
        self.tight = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.picker = ft.FilePicker()
        self.path = ""
        self.pwd = ft.TextField(
                            label="Contraseña de encriptación",
                            tooltip="Contraseña de encriptación",
                            border_color=th.ENC_COL,
                            prefix_icon=ft.Icon(icon=ft.Icons.LOCK_OUTLINE,
                                                    color=th.ENC_COL,
                                                    size=20), 
                            color = th.ENC_COL,
                            label_style = ft.TextStyle(color=th.ENC_COL))
        self.path_picker = ft.TextButton("Seleccionar carpeta destino",icon=ft.Icon(
                                                    icon=ft.Icons.DOWNLOAD,
                                                    color=th.DES_COL,
                                                    size=20,
                                                ),
            
                                            style=ft.ButtonStyle(
                                                color=th.DES_COL,
                                            ), on_click=self.set_path)
        self.path_label = ft.Text(
                            f"Ruta: {self.path}",
                            tooltip="Ruta o Path al archivo",
                            color = th.DES_COL,
                            )
        self.controls = [self.pwd, self.path_picker, self.path_label]
        
    
    def rem_path(self):
        self.path_label.visible = False
        self.path_picker.visible = False

    def get_pwd(self):
        return self.pwd.value
    
    def get_path(self):
        return self.path_label.value

    def reset_content(self):
        self.pwd.value = ''
        self.path_label.value = ''

    def set_theme(self, mode):
        if not mode :
            self.color = th.DES_COL
            for control in self.controls:
                if type(control) is ft.TextField:
                    control.border_color = th.DES_COL
                    control.color = th.DES_COL
                    control.label_style = ft.TextStyle(
                                            color=th.DES_COL
                    )
                    control.prefix_icon.color = th.DES_COL

    async def set_path(self):
        response = await self.picker.get_directory_path()
        if response:
            self.path = response
            self.path_label.value = response
        

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
        self.button = ft.TextButton(content = "Encriptar", on_click=self.encrypt, style=ft.ButtonStyle(
                                                color=th.ENC_COL,
                                            ))
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
                                            ),
                            color = th.ENC_COL,
                            label_style = ft.TextStyle(color=th.ENC_COL))
        self.usr = ft.TextField(
                            label="Usuario",
                            tooltip="Usuario activo en servidor SMTP",
                            border_color=self.border_color,
                            prefix_icon = ft.Icon(
                                                icon=ft.Icons.PERSON, 
                                                color=self.text_color,
                                                size=20
                                            ),
                            color = th.ENC_COL,
                            label_style = ft.TextStyle(color=th.ENC_COL))
        
        self.pwd = ft.TextField(
                            label="Contraseña",
                            tooltip="Contraseña de ervidor SMTP",
                            border_color=self.border_color,
                            prefix_icon = ft.Icon(
                                                icon=ft.Icons.LOCK_OUTLINE, 
                                                color=self.text_color,
                                                size=20
                                            ),
                            color = th.ENC_COL,
                            label_style = ft.TextStyle(color=th.ENC_COL))
        
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

    def _get_ip_add(self):
        return self.ip.value

    def _get_usr(self):
        return self.usr.value

    def _get_pwd(self):
        return self.pwd.value

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

    def _get_ip_add(self):
        return self.server_form._get_ip_add()

    def _get_usr(self):
        return self.server_form._get_usr()

    def _get_pwd(self):
        return self.server_form._get_pwd()
        
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
                                            ),
                                    color = th.ENC_COL,
                                    label_style = ft.TextStyle(color=th.ENC_COL))
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

    def _get_path(self):
        return self.content.value

@ft.control
class CloudUploadDialog(MainDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent_cmp = parent
        
    def init(self):
        self.title.color = th.ENC_COL
        self.connected = False
        self.bgcolor = th.ENC_BG
        self.card = ConnectionCard()
        self.file_location = PathCard()
        self.card.set_theme(True)
        self.content = ft.Column(horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                tight= True,
                                controls = [
                                    self.card,
                                    ft.Row(self.file_location)
                                    ]
                                )
        self.conect = ft.TextButton("Conectar", icon=ft.Icons.WIFI, on_click=self._connect)
        self.upload = ft.TextButton("Subir", icon=ft.Icons.UPLOAD, on_click=self._upload, disabled=True)
        self.actions = [self.conect, self.upload] 
        self.server = None

    def reset_dialog(self):
        self.card.reset_card()
        self.file_location.reset_content()
        self.upload.disabled = True
        if self.server is not None:
            self.server.desconectar()
        self.server = None

    def _connect(self):
        ip_add = self._get_ip_add()
        usr = self._get_usr()
        pwd = self._get_pwd()

        self.server = sftp.AdaptadorSFTP(ip_add)

        try:
            self.server.conectar(usr, pwd)
            self.upload.disabled = False
            self.parent_cmp.info_dialog.set_msg("Conexión exitosa!")
            self.page.show_dialog(self.parent_cmp.info_dialog)
        except Exception as e:
            self.parent_cmp.error_dialog.set_msg("No se pudo establecer la conexión con el servidor.")
            self.page.show_dialog(self.parent_cmp.error_dialog)        

    def _upload(self):
        path = self._get_path()
        data = self.parent_cmp.encr_file
        self.server.cargar(data, path)
        self.page.pop_dialog()
        self.parent_cmp.info_dialog.set_msg("Archivo cargado correctamente!")
        self.page.show_dialog(self.parent_cmp.info_dialog)
        self.server.desconectar()

    def _get_ip_add(self):
        return self.card._get_ip_add()

    def _get_usr(self):
        return self.card._get_usr()

    def _get_pwd(self):
        return self.card._get_pwd()
    
    def _get_path(self):
        return self.file_location._get_path()

@ft.control
class CloudDownloadDialog(MainDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent_cmp = parent

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
                                                    ), on_click=self._connect
                                    )

        self.download = ft.TextButton("Bajar",icon=ft.Icon(
                                                    icon=ft.Icons.DOWNLOAD,
                                                    color=th.DES_COL,
                                                    size=20,
                                                ),
            
                                            style=ft.ButtonStyle(
                                                color=th.DES_COL,
                                            ),
                                            disabled=True,
                                            on_click=self._download
                                        )
        self.actions = [self.conect, self.download] 
        self.server = None
    
    def reset_dialog(self):
        self.card.reset_card()
        self.file_location.reset_content()
        self.download.disabled = True
        if self.server is not None:
            self.server.desconectar()
        self.server = None

    def _connect(self):
        ip_add = self._get_ip_add()
        usr = self._get_usr()
        pwd = self._get_pwd()

        self.server = sftp.AdaptadorSFTP(ip_add)

        try:
            self.server.conectar(usr, pwd)
            self.download.disabled = False
            self.parent_cmp.info_dialog.set_msg("Conexión exitosa!")
            self.page.show_dialog(self.parent_cmp.info_dialog)
        except Exception as e:
            self.parent_cmp.error_dialog.set_msg("No se pudo establecer la conexión con el servidor.")
            self.page.show_dialog(self.parent_cmp.error_dialog)  

    def _download(self):
        path = self._get_path()
        data = self.server.descargar(path)
        self.page.pop_dialog()
        self.parent_cmp.info_dialog.set_msg("Archivo recuperado correctamente!")
        self.page.show_dialog(self.parent_cmp.info_dialog)
        self.server.desconectar()

        self.parent_cmp.set_encrypted(data, "left")


    def _get_ip_add(self):
        return self.card._get_ip_add()

    def _get_usr(self):
        return self.card._get_usr()

    def _get_pwd(self):
        return self.card._get_pwd()
    
    def _get_path(self):
        return self.file_location._get_path()

@ft.control
class LocalDownloadDialog(MainDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent_cmp = parent

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
                                            ),
                                            on_click=self.decrypt_download)
        self.actions = [self.button] 
    
    def reset_dialog(self):
        self.cont.reset_content()

    def decrypt_download(self):
        path = self._get_path()
        pwd = self._get_pwd()
        data = self.parent_cmp.encr_file

        try: 
            if path != "":
                file = AAA.decrypt(pwd, data)
                print(file) #TODO: imprimir esto en la right column del body
                """
                Ejemplo de como viene file: Archivo(metadata={'name': 'secreto.txt', 'weight': 42, 'path': 'C:\\Users\\NICOLAS\\Desktop\\secreto.txt', 'extension': '.txt'}, contenido=b'LA PISTOLA DE SILICONA SE QUED\xc3\x93 CONECTADA')
                """
                name = file.metadata["name"]

                with open(path+"\\" +name, 'wb') as archivo:
                    archivo.write(file.contenido)

                self.page.pop_dialog()
                self.parent_cmp.info_dialog.set_msg("Archivo desencriptado y guardado correctamente!")
                self.page.show_dialog(self.parent_cmp.info_dialog)
            else:
                raise Exception("Por favor, seleccione una carpeta para guardar el archivo desencriptado.")
        except Exception as e:
             self.parent_cmp.error_dialog.set_msg("No se pudo desencriptar el archivo. La contraseña puede ser incorrecta. " + str(e))
             self.page.show_dialog(self.parent_cmp.error_dialog) 

        

    def _get_path(self):
        return self.cont.get_path()

    def _get_pwd(self):
        return self.cont.get_pwd()

        


    
@ft.control
class ConnectionErrorDialog(ft.AlertDialog):
    def init(self):
        self.title : ft.Text = ft.Text("¡Ha habido un error!", color=th.ERROR_COL)
        self.content : ft.Text = ft.Text("")
        
        self.actions : list[ft.TextButton] = [ft.TextButton(content = "Aceptar", 
                                                            on_click=self._pop_me, 
                                                            style=ft.ButtonStyle(
                                                                color=th.ERROR_COL))] 
        self.open : bool = False
        self.bgcolor = th.ERROR_BG

    def _pop_me(self):
        self.page.pop_dialog()

    def set_msg(self, msg):
        self.content.value = msg

@ft.control
class ConnectionInfoDialog (ft.AlertDialog):
    def init(self):
        self.title : ft.Text =ft.Text("Información", color=th.INFO_COL)
        self.content : ft.Text = ft.Text("Si está leyendo esto, contacta a IT")
        
        self.actions : list[ft.TextButton] = [ft.TextButton(content = "Aceptar", 
                                                            on_click=self._pop_me, 
                                                            style=ft.ButtonStyle(
                                                                color=th.INFO_COL))]
        self.open : bool = False
        self.bgcolor = th.INFO_BG
    
    def _pop_me(self):
        self.page.pop_dialog()

    def set_msg(self, msg):
        self.content.value = msg