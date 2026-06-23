from flask import Flask, render_template, session, redirect

app = Flask(__name__)

app.secret_key = "lectosfera2026"


@app.route('/')
def inicio():
    return render_template("index.html")


libros = [
    {'id':1,'nombre':'1984','autor':'George Orwell','genero':'Distopía','precio':45000,'stock':10,'imagen':'https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg','descripcion':'Novela distópica que presenta una sociedad vigilada por el Gran Hermano.'},
    {'id':2,'nombre':'El Principito','autor':'Antoine de Saint-Exupéry','genero':'Fábula','precio':35000,'stock':8,'imagen':'https://covers.openlibrary.org/b/isbn/9780156012195-L.jpg','descripcion':'Historia poética sobre amistad, imaginación y el sentido de la vida.'},
    {'id':3,'nombre':'Clean Code','autor':'Robert Martin','genero':'Programación','precio':120000,'stock':5,'imagen':'https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg','descripcion':'Guía de buenas prácticas para escribir software mantenible.'},
    {'id':4,'nombre':'Don Quijote','autor':'Miguel de Cervantes','genero':'Clásico','precio':70000,'stock':7,'imagen':'https://covers.openlibrary.org/b/isbn/9780060934347-L.jpg'},
    {'id':5,'nombre':'Hábitos Atómicos','autor':'James Clear','genero':'Desarrollo personal','precio':65000,'stock':12,'imagen':'https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg'},
    {'id':6,'nombre':'Sapiens','autor':'Yuval Noah Harari','genero':'Historia','precio':85000,'stock':6,'imagen':'https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg'},
    {'id':7,'nombre':'Homo Deus','autor':'Yuval Noah Harari','genero':'Historia','precio':88000,'stock':4,'imagen':'https://covers.openlibrary.org/b/isbn/9780062464316-L.jpg'},
    {'id':8,'nombre':'Deep Work','autor':'Cal Newport','genero':'Productividad','precio':78000,'stock':9,'imagen':'https://covers.openlibrary.org/b/isbn/9781455586691-L.jpg'},
    {'id':9,'nombre':'Steve Jobs','autor':'Walter Isaacson','genero':'Biografía','precio':95000,'stock':5,'imagen':'https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg'},
    {'id':10,'nombre':'El Alquimista','autor':'Paulo Coelho','genero':'Novela','precio':42000,'stock':15,'imagen':'https://covers.openlibrary.org/b/isbn/9780061122415-L.jpg'},
    {'id':11,'nombre':'Padre Rico Padre Pobre','autor':'Robert Kiyosaki','genero':'Finanzas','precio':60000,'stock':10,'imagen':'https://covers.openlibrary.org/b/isbn/9781612680194-L.jpg'},
    {'id':12,'nombre':'Python Crash Course','autor':'Eric Matthes','genero':'Programación','precio':135000,'stock':4,'imagen':'https://covers.openlibrary.org/b/isbn/9781593279288-L.jpg'},
    {'id':13,'nombre':'Refactoring','autor':'Martin Fowler','genero':'Programación','precio':150000,'stock':3,'imagen':'https://covers.openlibrary.org/b/isbn/9780134757599-L.jpg'},
    {'id':14,'nombre':'Drácula','autor':'Bram Stoker','genero':'Terror','precio':40000,'stock':8,'imagen':'https://covers.openlibrary.org/b/isbn/9780486411095-L.jpg'},
    {'id':15,'nombre':'La Odisea','autor':'Homero','genero':'Clásico','precio':50000,'stock':6,'imagen':'https://covers.openlibrary.org/b/isbn/9780140268867-L.jpg'},
    {'id':16,'nombre':'Orgullo y Prejuicio','autor':'Jane Austen','genero':'Novela','precio':45000,'stock':9,'imagen':'https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg'},
    {'id':17,'nombre':'Cien años de soledad','autor':'Gabriel García Márquez','genero':'Novela','precio':68000,'stock':10,'imagen':'https://covers.openlibrary.org/b/isbn/9780307474728-L.jpg'},
    {'id':18,'nombre':'El arte de la guerra','autor':'Sun Tzu','genero':'Estrategia','precio':30000,'stock':20,'imagen':'https://covers.openlibrary.org/b/isbn/9781599869773-L.jpg'},
    {'id':19,'nombre':'Harry Potter','autor':'J. K. Rowling','genero':'Fantasía','precio':75000,'stock':7,'imagen':'https://covers.openlibrary.org/b/isbn/9780590353427-L.jpg'},
    {'id':20,'nombre':'El Señor de los Anillos','autor':'J. R. R. Tolkien','genero':'Fantasía','precio':110000,'stock':5,'imagen':'https://covers.openlibrary.org/b/isbn/9780618640157-L.jpg'}
]

pedidos = []
usuarios = []


@app.route('/catalogo')
def catalogo():
    from flask import request

    busqueda = request.args.get('q', '').lower()
    genero = request.args.get('genero', '').lower()
    precio_max = request.args.get('precio_max', '')

    resultados = libros

    if busqueda:
        resultados = [
            libro for libro in resultados
            if busqueda in libro['nombre'].lower()
        ]

    if genero:
        resultados = [
            libro for libro in resultados
            if genero in libro['genero'].lower()
        ]

    if precio_max:
        resultados = [
            libro for libro in resultados
            if libro['precio'] <= int(precio_max)
        ]

    return render_template(
        'catalogo.html',
        libros=resultados,
        busqueda=busqueda,
        genero=genero,
        precio_max=precio_max
    )
@app.route('/producto/<int:id>')
def producto(id):

    libro = next((l for l in libros if l['id']==id),None)

    if libro:

        return render_template(
                    'producto.html',
                    libro=libro
                )


    return "Libro no encontrado"




@app.route('/comprar/<int:id>')
def comprar(id):

    carrito = session.get('carrito', {})

    if not isinstance(carrito, dict):
        carrito = {}

    id = str(id)

    if id in carrito:
        carrito[id] += 1
    else:
        carrito[id] = 1

    session['carrito'] = carrito
    session.modified = True

    return redirect('/carrito')

@app.route('/carrito')
def carrito():

    carrito = session.get('carrito', {})

    items = []
    total = 0

    for id, cantidad in carrito.items():

        libro = next(
            (l for l in libros if l['id'] == int(id)),
            None
        )

        if libro:
            libro_copia = libro.copy()
            libro_copia['cantidad'] = cantidad
            libro_copia['subtotal'] = cantidad * libro['precio']

            total += libro_copia['subtotal']
            items.append(libro_copia)

    return render_template(
        'carrito.html',
        items=items,
        total=total
    )



@app.route('/vaciar_carrito')
def vaciar_carrito():
    session.pop('carrito', None)
    return redirect('/catalogo')

@app.route('/eliminar/<int:id>')
def eliminar(id):

    carrito = session.get('carrito',{})

    id = str(id)

    if id in carrito:

        carrito[id] -= 1

        if carrito[id] <= 0:
            del carrito[id]

    session['carrito'] = carrito
    session.modified = True

    return redirect('/carrito')

@app.route('/checkout')
def checkout():
    carrito = session.get('carrito', {})

    if not carrito:
        return redirect('/catalogo')

    return render_template('checkout.html')


@app.route('/pedido_confirmado')
def pedido_confirmado():

    carrito = session.get('carrito', {})
    items = []
    total = 0

    for id, cantidad in carrito.items():
        libro = next((l for l in libros if l['id'] == int(id)), None)

        if libro:
            libro_copia = libro.copy()
            libro_copia['cantidad'] = cantidad
            libro_copia['subtotal'] = cantidad * libro['precio']
            total += libro_copia['subtotal']
            items.append(libro_copia)

    pedido = {
        'id': len(pedidos) + 1,
        'items': items,
        'total': total
    }

    pedidos.append(pedido)
    session.pop('carrito', None)

    return render_template('pedido_confirmado.html', pedido=pedido)

@app.route('/pedidos')
def ver_pedidos():
    return render_template('pedidos.html', pedidos=pedidos)



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    from flask import request

    if request.method == 'POST':
        usuario = {
            'nombre': request.form['nombre'],
            'correo': request.form['correo'],
            'password': request.form['password']
        }

        usuarios.append(usuario)
        return redirect('/login')

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    from flask import request

    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        usuario = next(
            (
                u for u in usuarios
                if u['correo'] == correo and u['password'] == password
            ),
            None
        )

        if usuario:
            session['usuario'] = usuario['nombre']
            return redirect('/catalogo')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

