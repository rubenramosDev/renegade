
from multiprocessing import context
from ..bd import obtener_conexion
import uuid
from datetime import datetime
from ..config import USUARIO_CLIENTE, USUARIO_ADMIN
from .Queries.Productos import QueriesProducto as QueryProductos


class Cliente():

    def consultarCliente(self, id):
        try:
            query = 'SELECT * FROM usuario WHERE id=%s'
            conexion = obtener_conexion(USUARIO_CLIENTE)
            usuario = []

            with conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                usuario = cursor.fetchall()

            cursor.close()
            return usuario
        except Exception as ex:
            raise Exception(ex)

    def actualizarUsuario(self, nombre, apellidos, email, id):
        try:
            query = 'UPDATE usuario SET nombres = %s, apellidos = %s, correo = %s WHERE id = %s;'
            conexion = obtener_conexion(USUARIO_CLIENTE)

            with conexion.cursor() as cursor:
                cursor.execute(query, (nombre, apellidos, email,  id))

            conexion.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)

    def eliminar_producto(self, id):
        try:
            query = 'UPDATE usuario SET activo = 0 WHERE id = %s'
            conexion = obtener_conexion(USUARIO_ADMIN)

            with conexion.cursor() as cursor:
                cursor.execute(query, (id,))

            conexion.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)

    def generar_venta(self, id_cliente):
        try:
            self.calculo_stock(id_cliente)
            self.registrar_venta(id_cliente)
            self.desactivar_carrito_por_cliente(id_cliente)
            self.activar_carrito_por_cliente(id_cliente)
        except Exception as ex:
            raise Exception(ex)

    def registrar_venta(self, id_cliente):
        try:
            folio = str(uuid.uuid4())
            fecha = datetime.today().strftime('%Y-%m-%d')
            carrito = self.obtener_carrito_activo_cliente(id_cliente)
            total = self.calcular_total_carrito_compra(carrito[0])
            query = 'INSERT INTO venta(folio, total, fecha, idCarrito) VALUES (%s, %s, %s, %s);'
            conexion = obtener_conexion(USUARIO_ADMIN)

            with conexion.cursor() as cursor:
                cursor.execute(query, (folio, total, fecha, carrito[0]))

            conexion.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)

    def obtener_carrito_activo_cliente(self, id_cliente):
        try:
            query = 'SELECT id, status, idUsuario FROM carrito WHERE idUsuario = %s AND status = 1;'
            conexion = obtener_conexion(USUARIO_ADMIN)
            carrito = []

            with conexion.cursor() as cursor:
                cursor.execute(query, (id_cliente))
                carrito = cursor.fetchone()
                cursor.close()

            if carrito:
                return carrito

            raise Exception(
                "No existe un carrito de compras activo para el cliente.")
        except Exception as ex:
            raise Exception(ex)

    def desactivar_carrito_por_cliente(self, id_cliente):
        try:
            carrito = self.obtener_carrito_activo_cliente(id_cliente)
            query = 'UPDATE carrito SET status = 0 WHERE id = %s;'
            conexion = obtener_conexion(USUARIO_ADMIN)

            with conexion.cursor() as cursor:
                cursor.execute(query, (carrito[0]))

            conexion.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)

    def activar_carrito_por_cliente(self, id_cliente):
        try:
            query = 'INSERT INTO carrito(status, idUsuario) VALUES (1,%s);'
            conexion = obtener_conexion(USUARIO_ADMIN)

            with conexion.cursor() as cursor:
                cursor.execute(query, (id_cliente))

            conexion.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)

    def calcular_total_carrito_compra(self, carrito_id):
        try:
            query = 'SELECT sum(suma) FROM (SELECT SUM(cantidad * precio) AS suma FROM carrito  \
                    INNER JOIN productocarrito p on carrito.id = p.idCarrito WHERE idCarrito = %s  \
                    GROUP BY idProducto) AS total;'

            conexion = obtener_conexion(USUARIO_ADMIN)
            total = []

            with conexion.cursor() as cursor:
                cursor.execute(query, (carrito_id))
                total = cursor.fetchone()
                cursor.close()

            return total
        except Exception as ex:
            raise Exception(ex)

    def consulta_mis_ventas(self, idCliente):
        try:
            query = 'SELECT * FROM vista_carritos_usuario WHERE idUsuario=%s AND status=0'
            conexion = obtener_conexion(USUARIO_CLIENTE)
            carritos = []

            with conexion.cursor() as cursor:
                cursor.execute(query, (idCliente,))
                carritos = cursor.fetchall()

            conexion.commit()
            cursor.close()
            return carritos

        except Exception as e:
            raise Exception(e)

    def puede_comprar(self, id_usario):
        try:
            carrito = self.obtener_carrito_activo_cliente(id_usario)
            productos = self.consultar_productos_por_carrito(carrito[0])

            if len(productos) == 0:
                return False

            for producto in productos:
                if(int(producto[2]) < int(producto[1])):
                    return False

            return True
        except Exception as e:
            raise Exception(e)

    def consultar_productos_por_carrito(self, id_carrito):
        try:
            query = 'SELECT p2.id, p.cantidad, p2.stock FROM carrito \
                    INNER JOIN productocarrito p on carrito.id = p.idCarrito \
                    INNER JOIN renegade.producto p2 on p.idProducto = p2.id \
                    WHERE carrito.id = %s;'

            conexion = obtener_conexion(USUARIO_CLIENTE)
            productos = []

            with conexion.cursor() as cursor:
                cursor.execute(query, (id_carrito))
                productos = cursor.fetchall()

            conexion.commit()
            cursor.close()
            return productos

        except Exception as e:
            raise Exception(e)

    def calculo_stock(self, id_cliente):
        try:
            carrito = self.obtener_carrito_activo_cliente(id_cliente)
            productos = self.consultar_productos_por_carrito(carrito[0])

            for producto in productos:
                nueva_cantidad = int(producto[2]) - int(producto[1])
                self.descontar_stock(nueva_cantidad, producto[0])

        except Exception as e:
            raise Exception(e)

    def descontar_stock(self, nueva_cantidad, id_producto):
        try:
            query = 'UPDATE renegade.producto SET stock = %s WHERE id = %s;'
            conexion = obtener_conexion(USUARIO_ADMIN)

            with conexion.cursor() as cursor:
                cursor.execute(query, (nueva_cantidad, id_producto))
                conexion.commit()
                cursor.close()

        except Exception as e:
            raise Exception(e)
        
    def detalle_consulta_mis_ventas(self,idCarrito):
        try:
            query='SELECT * FROM vista_detalle_carrito WHERE idCarrito=%s'
            conexion= obtener_conexion(USUARIO_CLIENTE)
            productos=[]
            
            with conexion.cursor() as cursor:
                cursor.execute(query, (idCarrito,))
                productos = cursor.fetchall()
            
            conexion.commit()
            cursor.close()
            return productos
            
        except Exception as e:
            raise Exception(e)
