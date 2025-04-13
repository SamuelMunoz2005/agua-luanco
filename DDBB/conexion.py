import mysql.connector as mc
from mysql.connector import Error
from tkinter import messagebox as mg
class DDBB():
    def __init__(self):
        try:
            self.conn = mc.connect(
                host = 'localhost',
                user = 'root',
                password = '',
                database = 'bbdd_aguas'
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            mg.showerror('ERROR','La base de datos no esta activada por favor activar')

class Usuario():
    def InsertarUsuario(nombre,run,n_medidor):
        insertar = 'INSERT INTO `usuarios`(`run`, `usuario`, `n_medidor`) VALUES (%s,%s,%s)'
        datos = (run,nombre,n_medidor,)
        db = DDBB()
        db.cursor.execute(insertar,datos)
        db.conn.commit()
        db.conn.close()
        
    def geterAllCondi(nombre):
        consulta = 'SELECT * FROM `usuarios` WHERE usuario = %s'
        valor=(nombre,)
        db = DDBB()
        db.cursor.execute(consulta,valor)
        rows = db.cursor.fetchall()
        db.conn.close()
        return rows
    
    def geterAll():
        consulta = 'SELECT usuario FROM `usuarios`'
        db = DDBB()
        db.cursor.execute(consulta)
        rows = db.cursor.fetchall()
        db.conn.close()
        return rows
    
    def ObtenerTodoUsusario(run):
        consulta = 'SELECT * from usuarios u JOIN facturas f on(u.run = f.run) WHERE u.run = %s'
        dato = (run,)
        db = DDBB()
        db.cursor.execute(consulta,dato)
        rows = db.cursor.fetchall()
        db.conn.close()
        return rows

class Factura():
    def InsertarFactura(run,metros,fecha_factura,precio_total,metros_medidor):
        insertar = 'INSERT INTO `facturas`( `run`, `m3_consumidos`, `fecha_factura`, precio_total,metros_medidor) VALUES (%s,%s,%s,%s,%s)'
        datos = (run,metros,fecha_factura,precio_total,metros_medidor)
        db = DDBB()
        db.cursor.execute(insertar,datos)
        db.conn.commit()
        db.conn.close()
    def Crear_grafico(run):
        consulta = """ SELECT m3_consumidos, DATE_FORMAT(fecha_factura, '%M') 
                                AS mes_factura FROM facturas WHERE run = %s ORDER BY fecha_factura DESC LIMIT 4;"""
        persona = (run,)
        db = DDBB()
        db.cursor.execute("SET lc_time_names = 'es_ES';")
        db.cursor.execute(consulta,persona)
        rows = db.cursor.fetchall()
        db.conn.close()
        return rows
    def SacarMetrosAnterior(run):
        consulta = """ SELECT  metros_medidor FROM facturas WHERE run = %s ORDER BY fecha_factura DESC LIMIT 1;"""
        persona = (run,)
        db = DDBB()
        db.cursor.execute(consulta,persona)
        rows = db.cursor.fetchall()
        db.conn.close()
        return rows
     