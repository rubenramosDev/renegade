from itertools import product
from flask import Blueprint, g, redirect, render_template, request, url_for
from ..config import USUARIO_CLIENTE as USER_TYPE
from .Queries.CarritoProductos import QueriesCarrito as Query


cliente_carrito_name = "CLIENTE_CARRITO"
cliente_carrito_blueprint = Blueprint(cliente_carrito_name, __name__)


@cliente_carrito_blueprint.route("/cliente/carrito-productos/", methods=['GET'])
def carrito_productos():

    cliente = g.user.id

    query = Query()

    try:
        carrito_usuario = query.carrito_usuario(USER_TYPE, cliente)

        print(carrito_usuario)
        return render_template('/cliente/micarrito.html', carrito=carrito_usuario)
    except Exception as e:
        raise e


@cliente_carrito_blueprint.route("/cliente/eliminar-carrito/<id>", methods=['POST'])
def eliminar_producto_carrito(id):

    cliente = g.user.id
    producto = id
    carrito = request.form.get('carrito_id')

    query = Query()

    try:
        query.eliminar_producto_carrito(USER_TYPE, carrito, cliente, product)

        return redirect(url_for('cliente.CLIENTE_CARRITO.carrito_productos'))
    except Exception as e:
        raise e
