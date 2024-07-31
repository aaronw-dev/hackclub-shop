const storeName = '866e98-8d';
const accessToken = '1a0f8b8243b980d0407f15535f6518b2';
async function init() {
    const query = `
    {
    products(first: 4) {
        edges {
        node {
            id
            title
            description
            productType
            metafield(namespace: "custom", key: "short_description") {
                value
            }
            variants(first: 1) {
            edges {
                node {
                availableForSale
                }
            }
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
    }
    }
    `;
    var productData = {}
    await fetch(`https://${storeName}.myshopify.com/api/2024-07/graphql.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Shopify-Storefront-Access-Token': accessToken
        },
        body: JSON.stringify({ query })
    })
        .then(response => response.json())
        .then(data => productData = data)
        .catch(error => console.error('Error:', error));

    var products = productData.data.products.edges
    const productDiv = document.getElementById("allproducts")
    products.forEach(product => {
        /*
        <div class="shop-item">
            <img src="./images/products/forest_postcard.png">
            <div class="info">
                <span id="item-name">Our Forests Need Help</span>
                <p id="item-description">
                    Forests all over the world are burning down due to forest fires. Show your support!
                </p>
            </div>
            <button class="add-to-basket">Add to basket <img src="./images/icons/bag-full.svg"></button>
        </div>
        */
        console.log(product)
        const shortDescription = product.node.metafield ? product.node.metafield.value : '';
        const shopItem = document.createElement('div');
        shopItem.className = 'shop-item';

        const img = document.createElement('img');
        img.src = product.node.images.edges[0].node.src;
        shopItem.appendChild(img);

        const info = document.createElement('div');
        info.className = 'info';

        const itemName = document.createElement('span');
        itemName.id = 'item-name';
        itemName.textContent = product.node.title;
        info.appendChild(itemName);

        const itemDescription = document.createElement('p');
        itemDescription.id = 'item-description';
        itemDescription.innerHTML = shortDescription;
        info.appendChild(itemDescription);

        shopItem.appendChild(info);

        const button = document.createElement('button');
        button.className = 'add-to-basket';
        button.innerHTML = 'Add to basket <img src="./images/icons/bag-full.svg">';

        shopItem.appendChild(button);
        productDiv.appendChild(shopItem);
    })
    document.querySelectorAll(".shop-item>.add-to-basket").forEach(element => {
        element.addEventListener('mouseenter', function () {
            element.parentElement.querySelector('.info').classList.add('blurred');
        });

        element.addEventListener('mouseleave', function () {
            element.parentElement.querySelector('.info').classList.remove('blurred');
        });
    })
}

init()
