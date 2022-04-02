from ..bd import obtener_conexion
from ..config import USUARIO_ADMIN
import uuid


class Compras():

    def consultar_compras(self, tipo_usuario):
        try:
            query = 'SELECT * FROM vista_compras_surtidas;'
            conexion = obtener_conexion(tipo_usuario)
            materiasprimas = []

            with conexion.cursor() as cursor:
                cursor.execute(query)
                materiasprimas = cursor.fetchall()

            cursor.close()
            return materiasprimas
        except Exception as ex:
            raise Exception(ex)

    def consultar_compras_nosurtidas(self, tipo_usuario):
        try:
            query = 'SELECT * FROM vista_compras_nosurtidas;'
            conexion = obtener_conexion(tipo_usuario)
            materiasprimas = []

            with conexion.cursor() as cursor:
                cursor.execute(query)
                materiasprimas = cursor.fetchall()

            cursor.close()
            return materiasprimas
        except Exception as ex:
            raise Exception(ex)
        
    def consultar_compra_id(self, id):
        try:
            query = 'SELECT * FROM vista_compras_surtidas WHERE idOrdenCompra=%s;'
            conexion = obtener_conexion(USUARIO_ADMIN)
            materia = None

            with conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                materia = cursor.fetchone()

            cursor.close()
            return materia
        except Exception as ex:
            raise Exception(ex)
    
    def consultar_materias_compra(self, id):
        try:
            query = 'SELECT * FROM vista_lista_materias_compradas WHERE idOrdenCompra=%s;'
            conexion = obtener_conexion(USUARIO_ADMIN)
            materiasprimas = []

            with conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                materiasprimas = cursor.fetchall()

            cursor.close()
            return materiasprimas
        except Exception as ex:
            raise Exception(ex)
    
    def consultar_materia_select(self):
        try:
            query = 'SELECT * FROM MateriaPrima;'
            conexion = obtener_conexion(USUARIO_ADMIN)
            materiasprimas = []

            with conexion.cursor() as cursor:
                cursor.execute(query)
                materiasprimas = cursor.fetchall()

            cursor.close()
            return materiasprimas
        except Exception as ex:
            raise Exception(ex)
    
    def consultar_proveedor_select(self):
        try:
            query = 'SELECT * FROM Proveedor;'
            conexion = obtener_conexion(USUARIO_ADMIN)
            materiasprimas = []

            with conexion.cursor() as cursor:
                cursor.execute(query)
                materiasprimas = cursor.fetchall()

            cursor.close()
            return materiasprimas
        except Exception as ex:
            raise Exception(ex)

    def consultar_materia_id(self, id):
        try:
            query = 'SELECT m.*, com.costo FROM MateriaPrima  as m inner join \
                CompraStockMateria as com on m.id=com.idMateriaPrima\
                WHERE id=%s;'
            conexion = obtener_conexion(USUARIO_ADMIN)
            materia = None

            with conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                materia = cursor.fetchone()

            cursor.close()
            return materia
        except Exception as ex:
            raise Exception(ex)
    
    
    def asignarFolio(self):
        folio = str(uuid.uuid4())
        return folio
        
    
    def insertar_compra(self, tipo_usuario,folio, fecha, proveedor, listaMaterias):
        try:            
            query = 'INSERT INTO Compra (folio, idProveedor, fechaCompra) \
                    values (%s,%s,%s);'

            query2 = 'INSERT INTO CompraStockMateria (idOrdenCompra, idMateriaPrima, Cantidad, costo) \
                    values (%s,%s,%s,%s);'

            query3 = 'INSERT INTO StockMateriaPrima (cantidad, idMateriaPrima, idOrdenCompra) \
                    values (%s,%s,%s);'

            conexion = obtener_conexion(tipo_usuario)

            with conexion.cursor() as cursor:
                cursor.execute(query, (folio, proveedor, fecha))
            valCompraStockMateria = []
            valStockMateria = []
            idOrdenCompra = conexion.insert_id()

            for materia in listaMaterias:
                print(materia)
                list1 = (idOrdenCompra, int(materia['id']), int(
                    materia['cantidad']), materia['costo'])
                valCompraStockMateria.append(list1)
                
                print(valCompraStockMateria)

                for i in range(int(materia['cantidad'])):

                    list2 = (int(materia['cant']), int(
                        materia['id']), idOrdenCompra)
                    print("aqui estan los val de StockMateria .  . . . . .. . . . ")
                    print("aqui estan los val de StockMateria .  . . . . .. . . . ")
                    print("aqui estan los val de StockMateria .  . . . . .. . . . ")
                    print("aqui estan los val de StockMateria .  . . . . .. . . . ")
                    print("aqui estan los val de StockMateria .  . . . . .. . . . ")
                    valStockMateria.append(list2)
                    print(valStockMateria)

            with conexion.cursor() as cursor2:
                cursor2.executemany(query2, valCompraStockMateria)

            with conexion.cursor() as cursor3:
                cursor3.executemany(query3, valStockMateria)
            conexion.commit()

            cursor.close()

        except Exception as ex:
            raise Exception(ex)
        return
