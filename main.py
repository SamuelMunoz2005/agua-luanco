import os
import shutil
import locale
import tkinter as tk
from tkinter import ttk
from tkinter import TclError
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.pdfgen import canvas
from tkinter import messagebox as mg
from reportlab.lib.pagesizes import letter
from DDBB.conexion import Usuario,Factura 
from mysql.connector import errors, IntegrityError

class menu():
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('menu principal')
        self.ventana.config(bg='#4C6A92')
        self.directorio_actual = os.getcwd()
        self.ventana.iconbitmap(f"{self.directorio_actual}\\icons\\gota-de-agua.ico")
        screen_width = self.ventana.winfo_screenwidth()  
        screen_height = self.ventana.winfo_screenheight()
        self.ventana.geometry(f'{screen_width}x{screen_height}')
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.interior()
        self.ventana.mainloop()

    def interior(self):
        FrameIzquierdo = tk.Frame(self.ventana,width=400, height=900,bg='#6f8daa') 
        FrameIzquierdo.place(x=50,y=10)
        FrameIzquierdo.pack_propagate(False)
        Titulo = tk.Label(FrameIzquierdo,text='Comité de agua EL ESFUERZO LUANCO 2 ',font=('arial',15),bg='#6f8daa')
        Titulo.pack()
        AgreUsuLabel = tk.Label(FrameIzquierdo,text='Agregar Usuario',font=('arial',13),bg='#6f8daa')
        AgreUsuLabel.pack()
        AgreUsuBoton = tk.Button(FrameIzquierdo, text='agregar',font=('arial',13),command=self.crear_usuario,cursor='hand2',bg='#80b9c0')
        AgreUsuBoton.pack()

        CrearFacturaLabel = tk.Label(FrameIzquierdo,text='Crear Boleta',font=('arial',13),bg='#6f8daa')
        CrearFacturaLabel.pack()
        CrearFacturaBotan = tk.Button(FrameIzquierdo,text='Crear',font=('arial',13),command=self.CrearFactura,cursor='hand2',bg='#80b9c0')
        CrearFacturaBotan.pack()

        self.FrameDerecho = tk.Frame(self.ventana,width=850, height=900,bg='#77B8D6') 
        self.FrameDerecho.place(x=450,y=10)
        self.FrameDerecho.pack_propagate(False)

    def CrearFactura(self):
        self.limpiar_pantalla()

        lblCrearFactura = tk.Label(self.FrameDerecho,text='Crear Boleta',font=('arial',20),bg='#77B8D6')
        lblCrearFactura.pack()

        lblBuscarUsuario = tk.Label(self.FrameDerecho,text='Cual es el usuario que desea realizar la Boleta',font=('arial',13),bg='#77B8D6')
        lblBuscarUsuario.pack()
        clientes = [cliente[0] for cliente in Usuario.geterAll()]  
        self.cbBuscarUsuario = ttk.Combobox(self.FrameDerecho,font=('arial',13),state='readonly',value=clientes,)
        self.cbBuscarUsuario.pack()

        lblMetrosConsumidos= tk.Label(self.FrameDerecho,text='Cual fue la lectura del medidor ',font=('arial',13),bg='#77B8D6')
        lblMetrosConsumidos.pack()
        self.MetrosCosumidos = tk.IntVar()
        entryMetrosCosumidos = tk.Entry(self.FrameDerecho,textvariable=self.MetrosCosumidos,font=('arial',13))
        entryMetrosCosumidos.pack()

        self.fecha = tk.StringVar()
        lblFechaIngresada = tk.Label(self.FrameDerecho,text=' Fecha en que se realizo la boleta ', font=('arial',13),bg='#77B8D6')
        lblFechaIngresada.pack()
        EntryFecha = tk.Entry(self.FrameDerecho,textvariable=self.fecha, font=('arial',13))
        EntryFecha.pack()

        self.intereses = tk.IntVar()
        lblintereses = tk.Label(self.FrameDerecho,text='Cuantos intereses tiene el usuario', font=('arial',13),bg='#77B8D6')
        lblintereses.pack()
        EntryIntereses = tk.Entry(self.FrameDerecho,textvariable=self.intereses, font=('arial',13))
        EntryIntereses.pack()

        btnCrearFactura = tk.Button(self.FrameDerecho,text='crear', font=('arial',13),command=self.guardarFacturaBtn,cursor='hand2',bg='#80b9c0')
        btnCrearFactura.pack()

    def guardarFacturaBtn(self):
        try:
            usuario = self.cbBuscarUsuario.get()
            metros_medidor = self.MetrosCosumidos.get()
            fecha_str = self.fecha.get()
            intereses = self.intereses.get()
            fecha_hoy =  datetime.now()
            fecha_an = datetime.strptime(fecha_str,'%d-%m-%Y')

            if usuario =='' or metros_medidor == None or fecha_str =='' or intereses == None:
                mg.showerror('ERROR','Algunos de los campos están vacíos asegúrate que todos los campos estén completos')
            if fecha_an > fecha_hoy:
                mg.showerror('ERROR','No puedes ingresar fechas superior a la de la fecha actual')
            else:
                        fecha= fecha_an.strftime('%Y-%m-%d')
                        datos = Usuario.geterAllCondi(usuario)
                        run = datos[0][0]
                        numero_medidor = datos[0][2]
                        metros_antes=Factura.SacarMetrosAnterior(run)
                        self.directorio_clientes = f'{self.directorio_actual}\\usuarios de agua potable'
                        self.directorio_cliente = f'{self.directorio_clientes}\\{usuario}'
                        if not os.path.exists(self.directorio_clientes):
                                os.makedirs(self.directorio_clientes)  
                        if not os.path.exists(self.directorio_cliente):
                                os.makedirs(self.directorio_cliente)
                        metros_anter = 0  
                        if len(metros_antes) == 1:
                            metros_anter = metros_antes[0][0]
                        if metros_anter <= metros_medidor:
                            metro_pagar = abs(metros_medidor-metros_anter)
                            precio_total = (700*metro_pagar)+3000+intereses
                            Factura.InsertarFactura(run, metro_pagar, fecha,precio_total,metros_medidor,)
                            self.Crear_graficos(run,usuario)
                            pdf = self.Crear_pdf(usuario,run,numero_medidor,metros_medidor,precio_total,intereses,fecha,metros_anter,metro_pagar)
                            png_grafico = f'{self.directorio_actual}\\consumo de agua {usuario}.png'
                            os.remove(png_grafico)
                            factura = f'{self.directorio_actual}\\{pdf}'
                            directorio_mover = f'{self.directorio_actual}\\usuarios de agua potable\\{usuario}'
                            shutil.move(factura,directorio_mover)
                            metros_anter = 0  
                            metros_antes = []
                            mg.showinfo('INFO',f'Se agrego la boleta al usuario: {usuario} ')
                        else:
                            mg.showerror('ERROR','No puedes ingresar m3 menor a los m3 del mes anterior')
                            metros_anter = 0  
                            metros_antes = []
        except ValueError as e:
                    mg.showerror('ERROR', f'Error en el formato de los datos: {str(e)}. Por favor verifica los parámetros.')
                    metros_anter = 0  
                    metros_antes = []
        except TclError:
                    mg.showerror('ERROR', 'Error en los valores de entrada. Asegúrate de ingresar solo números enteros.')
                    metros_anter = 0  
                    metros_antes = []
        except Exception as e:
                    mg.showerror('ERROR', f'Ha ocurrido un error inesperado: {str(e)}')
                    metros_anter = 0  
                    metros_antes = []
       
    def crear_usuario(self):
        self.limpiar_pantalla()
        lblCrearUsuario = tk.Label(self.FrameDerecho,text='Crear o agregar cliente nuevo',font=('arial',20),bg='#77B8D6')
        lblCrearUsuario.pack()

        self.nombreUsuario = tk.StringVar()
        lblNombreUsuario = tk.Label(self.FrameDerecho,text='Ingresa el nombre del cliente ',font=('arial',13),bg='#77B8D6')
        lblNombreUsuario.pack()
        EntryNombreUsuario = tk.Entry(self.FrameDerecho,textvariable=self.nombreUsuario,font=('arial',13))
        EntryNombreUsuario.pack()

        self.RunUsuario = tk.StringVar()
        lblRunUsuario = tk.Label(self.FrameDerecho,text='Ingresa el run del cliente ',font=('arial',13),bg='#77B8D6')
        lblRunUsuario.pack()
        EntryRunUsuario = tk.Entry(self.FrameDerecho,textvariable=self.RunUsuario,font=('arial',13))
        EntryRunUsuario.pack()
        
        self.NumeroMedidor = tk.StringVar()
        lblNumeroMedidor = tk.Label(self.FrameDerecho,text='Ingresa el numero del medidor del cliente ',font=('arial',13),bg='#77B8D6')
        lblNumeroMedidor.pack()
        EntryNumeroMedidor = tk.Entry(self.FrameDerecho,textvariable=self.NumeroMedidor,font=('arial',13))
        EntryNumeroMedidor.pack()

        btonGuardarUsuario = tk.Button(self.FrameDerecho,text='guardar',font=('arial',13),command=self.BtnCrearUsuario,cursor='hand2',bg='#80b9c0')
        btonGuardarUsuario.pack()

    def BtnCrearUsuario(self):
        nombre =  self.nombreUsuario.get()
        run = self.RunUsuario.get()
        numero_medidor = self.NumeroMedidor.get()
        if nombre =='' or run =='' or numero_medidor =='':
             mg.showerror('ERROR','campos vacíos por favor ingresar datos')
        else:
            try:
                Usuario.InsertarUsuario(nombre,run,numero_medidor)
                self.directorio_clientes = f'{self.directorio_actual}\\usuarios de agua potable'
                self.directorio_cliente = f'{self.directorio_clientes}\\{nombre}'
                if not os.path.exists(self.directorio_clientes):
                        os.makedirs(self.directorio_clientes)  
                if not os.path.exists(self.directorio_cliente):
                        os.makedirs(self.directorio_cliente)
                mg.showinfo('INFO',f'Se ha agregado el usuario: {nombre} al sistema')
                
            except IntegrityError:
                mg.showerror('ERROR', 'El run o numero de medidor ya ingresados por favor revisar parámetros')

    def limpiar_pantalla(self):
        for i in self.FrameDerecho.winfo_children():
            i.destroy()

    def Crear_graficos(self,run,nombre):   
        cantidad_m3 = []
        mes = []
        contador = 0
        p = Factura.Crear_grafico(run)
        for i in p:
            contador += 1
            cantidad_m3.append(i[0])
            mes.append(i[1])
        bars = plt.bar(mes, cantidad_m3, color='skyblue', width=0.5)
        plt.title(f'Gráfico de consumo de agua de los últimos {contador} meses')
        plt.xlabel('Meses')
        plt.ylabel('cantidad de agua m3 en el medidor')
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
        plt.savefig(f"consumo de agua {nombre}.png")  
        plt.close()

    def Crear_pdf(self,nombre,run,numero_medidor,metros,precio_total,intereses,fecha_factura,metros_antes,metros_pagar):

        if isinstance(fecha_factura, str):
            fecha_obj = datetime.strptime(fecha_factura, "%Y-%m-%d")  
        else:
            fecha_obj = fecha_factura
        fecha = fecha_obj.strftime(" %B de %Y")
        
        ca = canvas.Canvas(filename=f'Boleta de {nombre} fecha {fecha}.pdf',pagesize=letter)
        ca.setFont('Helvetica',10)
        ca.drawString(x=250,y=770,text='BOLETA DE AGUA')
        ca.drawString(x=1,y=740,text='Comite de agua EL ESFUERZO LUANCO 2')
        ca.drawString(x=300,y=740,text=f'{fecha}                            _____/_____/_______/'.upper())
        data = [
                        ['','1 M3', '1.000 litros'],
                        [f'Usuario = {nombre}', 'M3 permitidos', '12.000 litros'],
                        [f'Run = {run}', 'cargo fijo', '$3.000'],
                        [f'Número Medidor = {numero_medidor}', 'valor m3', '$700'],
                        [' ', 'intereses sobre consumo', f'${intereses}'],
                        ['','Lectura medidor anterior',metros_antes],#falta que se actualice
                        ['','Lectura medidor actual',metros],#falta que se actualice
                        [' ', 'm3 consumidos mes', f'{metros_pagar} m3'],
                        [ 'cobros:'],
                        [ 'cargo fijo =', '$3.000'],
                        [ 'valor M3 consumidos', f'${metros_pagar * 700}'],
                        [ 'intereses=', f'${intereses}'],
                        [ 'total=', f'${precio_total}'],]
        
        self.dibujar_tabla(datos=data,x=1,y=700,columna_ancho=200,fila_alto=20,c=ca)
        ca.drawImage(f"consumo de agua {nombre}.png", x=1,y= 560, width=200, height=80)
        ca.drawString(x=410,y=480, text='___________________________________')
        ca.drawString(x=480,y=460,text='FIRMA USUARIO')

        #SEGUNDA BOLETA    
        ca.drawString(x=250,y=360,text='BOLETA DE AGUA')
        ca.drawString(x=1,y=340,text='Comite de agua EL ESFUERZO LUANCO 2')
        ca.drawString(x=300,y=340,text=f'{fecha}                            _____/_____/_______/'.upper())  
        self.dibujar_tabla(datos=data,x=1,y=300,columna_ancho=200,fila_alto=20,c=ca)
        ca.drawImage(f"consumo de agua {nombre}.png", x=1,y= 160, width=200, height=80)
        ca.drawString(x=410,y=100, text='___________________________________')
        ca.drawString(x=480,y=80,text='FIRMA USUARIO')      

        ca.save()

        return f'Boleta de {nombre} fecha {fecha}.pdf'

    def dibujar_tabla(self,datos, x, y, columna_ancho, fila_alto,c):
        for fila in datos:
            for i, celda in enumerate(fila):
                c.rect(x + i * columna_ancho, y, columna_ancho, fila_alto)  
                c.drawString(x + i * columna_ancho + 5, y + fila_alto / 2, str(celda))  
            y -= fila_alto  
menu()