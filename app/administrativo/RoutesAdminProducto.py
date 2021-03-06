from flask import Blueprint, g, session, flash, render_template, redirect, request, url_for
from .Queries.productoQuery import Producto
from ..site import UsuarioQueries
from ..config import USUARIO_ADMINISTATIVO


producto = Blueprint('producto', __name__, url_prefix='/admin')


@producto.before_request
def before_request_administrativo():
    if 'id' in session:
        model = UsuarioQueries()
        id = session['id']
        usuario = model.consultar_cliente_por_id(id)
        if usuario.idRol == 1:
            flash('No cuentas con permisos para consultar este módulo')
            return render_template('login.html')
        g.user = usuario
    else:
        flash('Es necesario inicar sesión para consultar este módulo')
        return render_template('login.html')


@producto.route("/productos")
def productos():
    query = Producto()
    lista_productos = query.consultarListaProductos(USUARIO_ADMINISTATIVO)
    return render_template('adm/administrativo/catalogo-productos.html', productos=lista_productos)


@producto.route("/productos/<product_id>")
def detalle_producto(product_id):
    query = Producto()
    producto = query.consultarProducto(USUARIO_ADMINISTATIVO, product_id)
    estructura = query.consultar_estructura_producto(product_id, USUARIO_ADMINISTATIVO)
    materias = query.consultarMateriaPrima(USUARIO_ADMINISTATIVO)
    return render_template('adm/administrativo/consulta-producto.html', producto=producto, estructura=estructura, materias=materias)


@producto.route("/detalle_producto/agregar", methods=['POST'])
def agregar_producto():
    name = request.form.get('nombre')
    desc = request.form.get('descripcion')
    talla = request.form.get('talla')
    image_url = request.form.get('image_url')
    query = Producto()
    resp = query.agregarProducto(name, desc, talla, image_url, USUARIO_ADMINISTATIVO)
    flash(resp)
    return redirect(url_for('administrativo.producto.productos'))


@producto.route("/detalle_producto/modificar", methods=['POST'])
def modificar_producto():
    product_id = int(request.form.get('id'))
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    talla = request.form.get('talla')
    image_url = request.form.get('image_url')
    cant_min = request.form.get('cant_min')
    cant_max = request.form.get('cant_max')
    query = Producto()
    resp = query.actualizarProducto(product_id, nombre, descripcion, talla, image_url, cant_min, cant_max,
                             USUARIO_ADMINISTATIVO)
    flash(resp)
    return redirect(url_for('administrativo.producto.detalle_producto', product_id=product_id))


@producto.route("/estructura_producto/agregar", methods=['POST'])
def agregar_materia_estructura():
    product_id = int(request.form.get('product_id'))
    materia_id = request.form.get('materia_id')
    descripcion = request.form.get('descripcion')
    cantidad = request.form.get('cantidad')
    query = Producto()
    query.agregar_materia_estructura(product_id, materia_id, cantidad, descripcion, USUARIO_ADMINISTATIVO)
    return redirect(url_for('administrativo.producto.detalle_producto', product_id=product_id))

@producto.route("/estructura_producto/<product_id>/del/<pieza_id>", methods=['POST'])
def eliminar_materia_estructura(product_id, pieza_id):
    query = Producto()
    resp = query.eliminar_materia_estructura(pieza_id, USUARIO_ADMINISTATIVO)
    flash(resp)
    return redirect(url_for('administrativo.producto.detalle_producto', product_id=product_id))


@producto.route("/detalle_producto/eliminar", methods=['POST'])
def eliminar_producto():
    product_id = int(request.form.get('id'))
    status = int(request.form.get('status'))
    query = Producto()
    query.estatus_producto(product_id, status, USUARIO_ADMINISTATIVO)
    return redirect(url_for('administrativo.producto.detalle_producto', product_id=product_id))