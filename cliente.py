import xmpp
import logging
from getpass import getpass
from argparse import ArgumentParser
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from aioconsole import ainput

def Registro():
    usuario = input("Ingresa el usuario a registrar: ")
    password = input("Contrasena: ")
    jid = xmpp.JID(usuario)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()

    if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
        return True
    else:
        return False       


class Cliente(slixmpp.ClientXMPP):

    def __init__(self, jid, password ):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)

        #Notificaciones
        self.add_event_handler("message", self.mensajes_recibidos)
        self.add_event_handler('got_online', self.usuario_se_conecto)
        self.add_event_handler('got_offline', self.usuario_se_desconecto)
        self.add_event_handler('presence_subscribed', self.usuario_te_agrego)
        self.add_event_handler('changed_status', self.usuario_cambio_estado)
  
    def usuario_cambio_estado(self, presencia):
        print("")
        if (str(presencia["from"]).split('/')[0]) != self.boundjid.bare:
            if presencia["show"]:
                print(presencia["from"], "actualizo su estatus a", presencia["show"])

    def usuario_te_agrego(self, presencia):
        print("")
        if (str(presencia["from"]).split('/')[0]) != self.boundjid.bare:
            print(presencia["from"], "te agrego como amigo")

    def usuario_se_desconecto(self, presencia):
        print("")
        if (str(presencia["from"]).split('/')[0]) != self.boundjid.bare:
          print(presencia["from"], "se desconecto")

    def usuario_se_conecto(self, presencia):
        print("")
        if (str(presencia["from"]).split('/')[0]) != self.boundjid.bare:
            print(presencia["from"], "esta en linea")

    def mensajes_recibidos(self, msg):
        if msg['type'] in ('chat', 'normal'):
            if len(msg['body']) > 1024:
                recv = msg['body'].encode()
                img_name = "img.jpg"
                with open(img_name, "wb") as dt:
                    dt.write(recv) 
                dt.close()
                print("\n")
                print("Imagen recibida de", str(msg['from']).split('/')[0])
            else:
                print("\n")
                print("Mensaje de:",str(msg['from']).split('/')[0])
                print("Contenido:", msg["body"])
        elif msg['type'] in ('groupchat', 'normal'):
            print("\n")
            print("Mensaje de grupo:",str(msg['from']).split('/')[0])
            print("Alias:",str(msg['from']).split('/')[1])
            print("Contenido:", msg["body"])

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        
        menu2 = '1. Mostrar usuarios y su estado \n2. Agregar usuario a los contactos\n3. Mostrar detalles de un usuario\n4. Comunicacion 1 a 1 con cualquier usuario\n5. Participar en conversaciones grupales\n6. Definir mensaje de presencia\n7. Enviar archivos\n8. Cerrar Sesion\n9. Eliminar cuenta'
        bandera = True
        print("")
        print("-------------------------Bienvenido-------------------------")
        while bandera:
            print("")
            print(menu2)
            print("")
            opcion = await ainput("Ingrese el numero de opcion a elegir: ")
            opcion = int(opcion)
            print("")
            if (opcion == 1):
                self.Mostrar_contactos()        
            elif (opcion == 2):
                usuario = await ainput("Usuario: ")
                self.Nuevo_contacto(usuario)
            elif (opcion == 3):
                usuario_informacion = await ainput('Ingrese el usuario de interes:  ')
                print("")
                self.Mostrar_contacto(usuario_informacion)        
            elif (opcion == 4):
                recipiente = await ainput('Ingrese el usuario destino: ')
                mensaje = await ainput('Ingrese el mensaje a enviar: ')
                self.Enviar_mensaje(recipiente, mensaje)
            elif (opcion == 5):
                    submenu = "1. Unirse a grupo\n2. Enviar chat grupal"
                    print(submenu)
                    opcion = await ainput("Ingrese el numero de opcion a elegir: ")
                    opcion = int(opcion)
                    if(opcion ==1):
                     print("")
                     grupo = await ainput('Ingrese el grupo para unirte: ')
                     alias = await ainput('Ingrese su alias: ')
                     self.Unirse_a_grupo(grupo, alias)
                    elif(opcion==2):
                        recipiente = await ainput('Ingrese el grupo destino: ')
                        mensaje = await ainput('Ingrese el mensaje a enviar: ')
                        self.Enviar_mensaje_a_grupo(recipiente, mensaje)
                        
            elif (opcion == 6):
                estado =  await ainput("Ingrese el estado a mostrar ej:[chat, away, xa, dnd]: ")
                mensaje_presencia =  await ainput("Igrese el mensaje de presencia: ")
                print("")
                self.Mensaje_presencia(estado, mensaje_presencia)
            elif (opcion == 7):
                archivo = await ainput('Ingrese el nombre del archivo: ')
                recipiente = await ainput('Ingrese el usuario destino: ') 
                self.Enviar_archivo(archivo, recipiente)
            elif (opcion == 8):
                self.disconnect()
                bandera = False
            elif (opcion == 9):
                self.Eliminar_cuenta()

            await self.get_roster()

    def Enviar_archivo(self, archivo, destino):
        inf =  open(archivo, 'rb')
        datos = inf.read()
        #print(datos)

        try:
            self.send_message(mto=destino, mbody=(str(datos)), mtype='chat')
            print('Se envio el archivo')
            print("")
        except IqError:
            print('Error al enviar el archivo')
        except IqTimeout:
            print('No hay respuesta del server')


    def Unirse_a_grupo(self, grupo, alias):
        self.plugin['xep_0045'].join_muc(grupo, alias)
        print("Ahorar perteneces al grupo")
        print("")

    def Enviar_mensaje_a_grupo(self, recipiente, mensaje):
        try:
            self.send_message(mto=recipiente, mbody=mensaje, mtype='groupchat')
            print('Se envio el mensaje')
            print("")
        except IqError:
            print('Error al enviar el mensaje')
        except IqTimeout:
            print('No hay respuesta del server')



    def Eliminar_cuenta(self):
        response = self.Iq()
        response['type'] = 'set'
        response['from'] = self.boundjid.user
        response['register']['remove'] = True
        try:
            response.send()
            print("Cuenta eliminada")
            self.disconnect()
        except IqError:
            print("Error al eliminar la cuenta")
            self.disconnect()
        except IqTimeout:
            print("No hay respuesta del server")
            self.disconnect()

    def Mensaje_presencia(self, estado, mensaje):
        self.send_presence(pshow=estado, pstatus=mensaje)

    def Mostrar_contacto(self, usuario):
        conexiones = self.client_roster.presence(usuario)
        for cliente, estado in conexiones.items():
            print('Usuario: ',usuario)
            print('Estado:  ',estado['status'])
        print("")

    def Mostrar_contactos(self):
        contactos = self.client_roster.groups()
        for contacto in contactos:
            for usuario in contactos[contacto]:
                if usuario != self.boundjid.bare:
                    print('Usuario: ',usuario)

                    conexiones = self.client_roster.presence(usuario)
                    for cliente, estado in conexiones.items():
                        if(estado['status']):
                            print('Estado:  ',estado['status'])
                    print("")

    def Enviar_mensaje(self, recipiente, mensaje):
        try:
            self.send_message(mto=recipiente, mbody=mensaje, mtype='chat')
            print('Se envio el mensaje')
            print("")
        except IqError:
            print('Error al enviar el mensaje')
        except IqTimeout:
            print('No hay respuesta del server')


    def Nuevo_contacto(self, usuario):
        self.send_presence_subscription(pto=usuario)

if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=Cliente.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel, format='%(levelname)-8s %(message)s')
    #logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

    menu1 = '1. Registrar nueva cuenta \n2. Iniciar Sesion'
    print(menu1)
    print("")
    opcion = int(input("Ingrese el numero de opcion a elegir: "))
    print("")
    if (opcion == 1):
        if Registro():
            print("Cuenta creada exitosammente")
        else:
            print("Error al crear la cuenta")

    elif(opcion == 2):
        args.jid = input("Usuario: ")
        args.password = input("Contrasena: ")
        xmpp = Cliente(args.jid, args.password)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0004') # Data Forms
        xmpp.register_plugin('xep_0060') # PubSub
        xmpp.register_plugin('xep_0199') # XMPP Ping    
        xmpp.register_plugin('xep_0066') # XMPP Ping    
        xmpp.register_plugin('xep_0085') # Chat State Notifications
        xmpp.register_plugin('xep_0066') # Out of Band Data
        xmpp.register_plugin('xep_0077') # In-Band Registration
        xmpp.register_plugin('xep_0045') # Multi-User Chat

        xmpp.connect(disable_starttls=True)
        xmpp.process(forever=False)
                  

                                                        