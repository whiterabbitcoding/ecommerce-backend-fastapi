from sql_app import models
from sql_app.database import engine
from sqlalchemy.orm import sessionmaker


def create_line_items(cart):
    cart_items = cart.cartitems
    line_items = [
        {"price": item.item.stripe_key, "quantity": item.quantity}
        for item in cart_items
    ]
    print(f"line_items for stripe - {line_items}")
    return line_items

def prepopulatedb():
    Session = sessionmaker(bind=engine)
    session = Session()
    products = [
        {
            "id": "prod_NlthGcR8UPfA1Y",
            "object": "product",
            "active": True,
            "attributes": [],
            "created": 1682329305,
            "default_price": "price_1N0Lu2IlhbmBVpcGDp5e0cDh",
            "description": "The third cassette",
            "images": [
                "https://files.stripe.com/links/MDB8YWNjdF8xSkhsQUZJbGhibUJWcGNHfGZsX3Rlc3RfdXBYaUpFMFdjVXRNamdwRUMxV0l0azRj008eOIMEME"
            ],
            "livemode": False,
            "metadata": {},
            "name": "Test Cassette 3",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682329306,
            "url": None,
        },
        {
            "id": "prod_NltgvCcc1z78mb",
            "object": "product",
            "active": True,
            "attributes": [],
            "created": 1682329272,
            "default_price": "price_1N0LtUIlhbmBVpcG93g1UJsD",
            "description": "Another cassette",
            "images": [
                "https://files.stripe.com/links/MDB8YWNjdF8xSkhsQUZJbGhibUJWcGNHfGZsX3Rlc3RfZjk5a1ZVbjM2aDl6VVdoaDN4MGN1dkVO006Z0SQjoH"
            ],
            "livemode": False,
            "metadata": {},
            "name": "Test Cassete 2",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682329272,
            "url": None,
        },
        {
            "id": "prod_Nltg9FyIihZ59o",
            "object": "product",
            "active": True,
            "attributes": [],
            "created": 1682329242,
            "default_price": "price_1N0Lt1IlhbmBVpcGGVtmh71F",
            "description": "A test cassette",
            "images": [
                "https://files.stripe.com/links/MDB8YWNjdF8xSkhsQUZJbGhibUJWcGNHfGZsX3Rlc3RfeU1yQnZ4NTRFV2NLSXlJRUZGQmx4NmVX00O6YeafVQ"
            ],
            "livemode": False,
            "metadata": {},
            "name": "Test Cassette 4",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682329673,
            "url": None,
        },
        {
            "id": "prod_NltbbA2VTPomIk",
            "object": "product",
            "active": True,
            "attributes": [],
            "created": 1682328955,
            "default_price": "price_1N0LoNIlhbmBVpcGDquJhCnr",
            "description": "A colourful keyboard ",
            "images": [
                "https://files.stripe.com/links/MDB8YWNjdF8xSkhsQUZJbGhibUJWcGNHfGZsX3Rlc3RfUGxyQ3hOWXhPZ2x4VkcwcGhSanJoVWow00zz9i2DXV"
            ],
            "livemode": False,
            "metadata": {},
            "name": "Lofi Keyboard",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682328956,
            "url": None,
        },
        {
            "id": "prod_NltaR3dkoBp3b3",
            "object": "product",
            "active": True,
            "attributes": [],
            "created": 1682328915,
            "default_price": "price_1N0LnjIlhbmBVpcGqMysSmGz",
            "description": "A lofi hoodie",
            "images": [
                "https://files.stripe.com/links/MDB8YWNjdF8xSkhsQUZJbGhibUJWcGNHfGZsX3Rlc3RfSEd3a0NRcEs0VWJGTU5razBEVFJ1N2tR00nsVdNA45"
            ],
            "livemode": False,
            "metadata": {},
            "name": "Lofi Hoodie 1",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682329377,
            "url": None,
        },
        {
            "id": "prod_NLfY6t2hUXjh0w",
            "object": "product",
            "active": False,
            "attributes": [],
            "created": 1676280079,
            "default_price": "price_1MayDsIlhbmBVpcGOCLD9DL3",
            "description": "The second lofi cassette by this geez.",
            "images": [],
            "livemode": False,
            "metadata": {},
            "name": "Cassette 2",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682329626,
            "url": None,
        },
        {
            "id": "prod_NLfY0FitTv2GaS",
            "object": "product",
            "active": True,
            "attributes": [],
            "created": 1676280042,
            "default_price": "price_1MayDHIlhbmBVpcG4YS74QZ9",
            "description": "A lofi cassette, the first",
            "images": [
                "https://files.stripe.com/links/MDB8YWNjdF8xSkhsQUZJbGhibUJWcGNHfGZsX3Rlc3RfYXJDYkpZWEV0UnJ2ajVVZTBqU0ZWcEhR00xCSVjEVD"
            ],
            "livemode": False,
            "metadata": {},
            "name": "Test Cassette 1",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682329658,
            "url": None,
        },
        {
            "id": "prod_JvmLMdefpIFXNe",
            "object": "product",
            "active": False,
            "attributes": [],
            "created": 1627409645,
            "default_price": None,
            "description": None,
            "images": [],
            "livemode": False,
            "metadata": {},
            "name": "Donation",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "type": "service",
            "unit_label": None,
            "updated": 1682329358,
            "url": None,
        },
    ]
    for product in products:
        session.add(
            models.Item(
                title=product.get("name"),
                description=product.get("description"),
                artist=product.get("name"),
                price=product.get("default_price"),
                stripe_key=product.get("default_price"),
                stock=10,
                product_information_url="product info url",
                music_url=f"music_url",
                image_url=product.get("images")[0]
                if len(product.get("images")) >= 1
                else None,
                product_type="string",
                stripe_product_key=product.get("id"),
            )
        )
        session.commit()
        session.close()
