from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from DDBB.conexion import Factura

metros_antes=Factura.SacarMetrosAnterior('88.458.658')
metros = []
for i in metros_antes:
      for e in i:
            metros.append(e)
metros_anter = metros[1]
print(metros_anter)

def Crear_pdf(usuario,run,numero_medidor,metros,precio_total,intereses,fecha_factura,metros_antes):
        ca = canvas.Canvas(filename=f'Factura de {usuario}.pdf',pagesize=letter)
        ca.setFont('Helvetica',10)

        ca.drawString(x=250,y=770,text='BOLETA DE AGUA')
        ca.drawString(x=1,y=740,text='Comite de agua EL ESFUERZO LUANCO 2')
        ca.drawString(x=380,y=740,text=fecha_factura)
        data = [
                        ['','1 M3', '1.000 litros'],
                        [f'Usuario = {usuario}', 'M3 permitidos', '12.000 litros'],
                        [f'Run = {run}', 'cargo fijo', '$3.000'],
                        [f'Número Medidor = {numero_medidor}', 'valor m3', '$700'],
                        [' ', 'intereses sobre consumo', f'${intereses}'],
                        ['','Lectura medidor anterior',metros_antes],#falta que se actualice
                        ['','Lectura medidor actual',abs(metros_antes-metros)],#falta que se actualice
                        [' ', 'm3 consumidos mes', f'{metros} m3'],
                        [ 'cobros:'],
                        [ 'cargo fijo =', '$3.000'],
                        [ 'valor M3 consumidos', f'${metros * 700}'],
                        [ 'intereses=', f'${intereses}'],
                        [ 'total=', f'${precio_total}'],]
        
        dibujar_tabla(datos=data,x=1,y=700,columna_ancho=200,fila_alto=20,c=ca)
        ca.drawImage(f"consumo de agua.png", x=1,y= 560, width=200, height=80)
        ca.drawString(x=410,y=480, text='___________________________________')
        ca.drawString(x=500,y=460,text='FIRMA')

        #SEGUNDA BOLETA 
        ca.drawString(x=250,y=400,text='BOLETA DE AGUA')
        ca.drawString(x=1,y=380,text='Comite de agua EL ESFUERZO LUANCO 2')

        ca.drawString(x=380,y=380,text=fecha_factura)  
        dibujar_tabla(datos=data,x=1,y=340,columna_ancho=200,fila_alto=20,c=ca)
        ca.drawImage(f"consumo de agua.png", x=1,y= 230, width=200, height=80)
        ca.drawString(x=410,y=120, text='___________________________________')
        ca.drawString(x=500,y=100,text='FIRMA')    

        ca.save()

def dibujar_tabla(datos, x, y, columna_ancho, fila_alto,c):
        for fila in datos:
            for i, celda in enumerate(fila):
                c.rect(x + i * columna_ancho, y, columna_ancho, fila_alto)  # Dibujar las celdas
                c.drawString(x + i * columna_ancho + 5, y + fila_alto / 2, str(celda))  # Dibujar el texto dentro de la celda
            y -= fila_alto

Crear_pdf(usuario='samuel alexis muñoz muñoz',run='21568',numero_medidor='897465',metros=8,precio_total=9876435,intereses=0,fecha_factura='07-04-2024',metros_antes=10)