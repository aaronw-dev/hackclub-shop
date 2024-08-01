from flask import Flask, render_template, make_response
import requests
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__,
            static_url_path='/resources',
            static_folder='static',
            template_folder='templates')

store_name = '866e98-8d'
access_token = '1a0f8b8243b980d0407f15535f6518b2'
graphql_endpoint = f'https://{store_name}.myshopify.com/api/2024-07/graphql.json'


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@nocache
@app.route('/')
def home():
    return render_template("index.html")


@nocache
@app.route('/product/<id>')
def product(id):
    query = """
    {
        product(id: "gid://shopify/Product/%s") {
            id
            title
            description
            productType
            variants(first: 10) {
            edges {
                node {
                    id
                    title
                    priceV2 {
                        amount
                        currencyCode
                    }
                    quantityAvailable
                }
            }
            }
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
    variants = [item["node"]
                for item in productinfo["variants"]["edges"]]
    description = productinfo["description"]
    shortdescription = productinfo["metafield"]["value"]
    title = productinfo["title"]
    stock = str(variants[0]["quantityAvailable"])
    imageurl = productinfo["images"]["edges"][0]["node"]["src"]
    pricedict = productinfo["variants"]["edges"][0]["node"]["priceV2"]
    price = f"${float(pricedict['amount']):.2f} {pricedict['currencyCode']}"
    return render_template("product.html", PRODUCT_DESCRIPTION=description, PRODUCT_TITLE=title, PRODUCT_STOCK=stock, PRODUCT_MAINIMAGE=imageurl, SHORT_DESCRIPTION=shortdescription, PRODUCT_PRICE=price)


@ app.route('/about')
def about():
    return 'About'
