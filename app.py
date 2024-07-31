from flask import Flask, render_template
import requests

app = Flask(__name__,
            static_url_path='/resources',
            static_folder='static',
            template_folder='templates')

store_name = '866e98-8d'
access_token = '1a0f8b8243b980d0407f15535f6518b2'
graphql_endpoint = f'https://{store_name}.myshopify.com/api/2024-07/graphql.json'


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/product/<id>')
def product(id):
    query = """
    {
        product(id: "gid://shopify/Product/%s") {
            id
            title
            description
            productType
            metafield(namespace: "custom", key: "short_description") {
                value
            }
            images(first: 1) {
            edges {
                node {
                src
                }
            }
            }
        }
    }
    """ % id
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Storefront-Access-Token': access_token
    }

    response = requests.post(graphql_endpoint, json={
                             'query': query}, headers=headers)
    productinfo = response.json()["data"]["product"]
    print(productinfo)
    description = productinfo["description"]
    shortdescription = productinfo["metafield"]["value"]
    title = productinfo["title"]
    stock = "150,000"
    imageurl = productinfo["images"]["edges"][0]["node"]["src"]
    return render_template("product.html", PRODUCT_DESCRIPTION=description, PRODUCT_TITLE=title, PRODUCT_STOCK=stock, PRODUCT_MAINIMAGE=imageurl, SHORT_DESCRIPTION=shortdescription)


@app.route('/about')
def about():
    return 'About'
