from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key'

API_URL = "https://fakestoreapi.com/products"

@app.route('/')
def index():
    response = requests.get(API_URL)
    products = response.json()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    response = requests.get(f"{API_URL}/{product_id}")
    product = response.json()
    return render_template('product_detail.html', product=product)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query'].lower()
        response = requests.get(API_URL)
        products = response.json()
        filtered_products = [p for p in products if query in p['title'].lower()]
        return render_template('search.html', products=filtered_products, query=query)
    return render_template('search.html', products=[])

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)  # Menghapus satu instance product_id
        session.modified = True
    return redirect(url_for('checkout'))

@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        return render_template('checkout.html', cart_items=[], total=0)
    
    cart_items = []
    total = 0
    for product_id in session['cart']:
        response = requests.get(f"{API_URL}/{product_id}")
        product = response.json()
        cart_items.append(product)
        total += product['price']
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)