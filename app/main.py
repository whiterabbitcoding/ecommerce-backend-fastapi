#! /usr/bin/env python3.6

import os
import stripe
from typing import Optional, List
from fastapi import FastAPI, Header, HTTPException, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware

import formulas
import helpers


from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Setup Stripe python client library.
load_dotenv(find_dotenv())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For sample support and debugging, not required for production:
stripe.set_app_info(
    "stripe-samples/accept-a-payment/prebuilt-checkout-page",
    version="0.0.1",
    url="https://github.com/stripe-samples",
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = "2020-08-27"
static_dir = str(os.path.abspath(os.path.join(__file__, "../../static")))

templates = Jinja2Templates(directory="static")

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def get_example(request: Request, db: Session = Depends(get_db), cart: int = None):
    products = [product.__dict__ for product in crud.get_items(db)]
    cart_output = crud.get_cart(db, cart) if cart else None
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products": products,
            "cart": crud.get_cart(db, cart) if cart else None,
            "total": formulas.get_total_for_cart(cart_output) if cart else 0,
        },
    )


@app.get("/product/{id}", response_class=HTMLResponse)
async def get_product(request: Request, id: str, db: Session = Depends(get_db)):
    product = crud.get_item(db, id)
    return templates.TemplateResponse(
        "product.html", {"request": request, "product": product}
    )


@app.post("/add-to-cart/")
def add_to_cart(
    request: Request,
    item_id: str = None,
    cart_id: str = None,
    db: Session = Depends(get_db),
):
    cart = None
    if cart_id == None:
        cart = crud.create_cart(db, item_id)
    crud.add_to_cart(db, cart_id, item_id)
    cart = cart_id
    return cart


@app.post("/add-to-cart-refresh/")
def add_to_cart_refresh(
    request: Request,
    item_id: str = None,
    cart_id: str = None,
    remove: bool = False,
    db: Session = Depends(get_db),
):
    cart = None
    if cart_id == None:
        cart = crud.create_cart(db, item_id)
        cart_id = cart.id
    if cart_id == None:
        print("gottem")
    crud.add_to_cart(db, cart_id, item_id, remove)
    cart = cart_id
    response = RedirectResponse(url=f"/?cart={cart_id}")
    response.status_code = 302
    return response


#  For react frontend
@app.post("/add-to-cart-new/")
def add_to_cart_new(
    request: Request,
    item_id: str = None,
    cart_id: str = None,
    remove: bool = False,
    db: Session = Depends(get_db),
):
    if cart_id == "null":
        print("Null given for cart ID")
        cart_id = None

    cart = None
    if cart_id == None:
        cart = crud.create_cart(db, item_id)
        cart_id = cart.id
    crud.add_to_cart(db, cart_id, item_id, remove)
    cart = cart_id
    return {"cart_id": cart_id}, 200


@app.get("/cart/{cart_id}")
def read_cart(
    cart_id: int,
    db: Session = Depends(get_db),
):
    cart_output = crud.get_cart(db, cart_id) if cart_id else None
    if cart_output:
        return cart_output
    else:
        return "failed"


@app.get("/item/{item_id}")
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item_output = crud.get_item(db, item_id) if item_id else None
    if item_output:
        return item_output
    else:
        return "failed"


# Fetch the Checkout Session to display the JSON result on the success page
@app.get("/checkout-session", response_model=stripe.checkout.Session)
def get_checkout_session(sessionId: str):
    id = sessionId
    checkout_session = stripe.checkout.Session.retrieve(id)
    return checkout_session


@app.post("/create-checkout-session")
def create_checkout_session():
    domain_url = os.getenv("DOMAIN")
    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url
            + "/static/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/static/canceled.html",
            payment_method_types=(os.getenv("PAYMENT_METHOD_TYPES") or "card").split(
                ","
            ),
            mode="payment",
            shipping_address_collection={"allowed_countries": ["US", "CA"]},
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 0, "currency": "usd"},
                        "display_name": "Free shipping",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 5},
                            "maximum": {"unit": "business_day", "value": 7},
                        },
                    },
                },
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 1500, "currency": "usd"},
                        "display_name": "Next day air",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 1},
                            "maximum": {"unit": "business_day", "value": 1},
                        },
                    },
                },
            ],
            line_items=[
                {
                    "price": os.getenv("PRICE_2"),
                    "quantity": 1,
                }
            ],
        )
        return RedirectResponse(checkout_session.url, status.HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(403, str(e))


@app.post("/create-checkout-session-new/")
def create_checkout_session(cart, db: Session = Depends(get_db)):
    domain_url = os.getenv("DOMAIN")
    try:
        # Create new Checkout Session for the order
        # Other optional params include:

        # For full details see https:#stripe.com/docs/api/checkout/sessions/create
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            line_items=helpers.create_line_items(crud.get_cart(db, cart)),
            success_url=domain_url
            + "/static/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/static/canceled.html",
            payment_method_types=(os.getenv("PAYMENT_METHOD_TYPES") or "card").split(
                ","
            ),
            mode="payment",
            shipping_address_collection={"allowed_countries": ["GB"]},
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 0, "currency": "gbp"},
                        "display_name": "Free shipping",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 5},
                            "maximum": {"unit": "business_day", "value": 7},
                        },
                    },
                },
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 1500, "currency": "gbp"},
                        "display_name": "Next day air",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 1},
                            "maximum": {"unit": "business_day", "value": 1},
                        },
                    },
                },
            ],
        )
        return RedirectResponse(checkout_session.url, status.HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(403, str(e))


@app.post("/create-checkout-session-react/")
def create_checkout_session_react(cart, db: Session = Depends(get_db)):
    domain_url = os.getenv("DOMAIN")
    try:
        # Create new Checkout Session for the order
        # Other optional params include:

        # For full details see https:#stripe.com/docs/api/checkout/sessions/create
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            line_items=helpers.create_line_items(crud.get_cart(db, cart)),
            success_url=domain_url
            + "/static/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/static/canceled.html",
            payment_method_types=(os.getenv("PAYMENT_METHOD_TYPES") or "card").split(
                ","
            ),
            mode="payment",
            shipping_address_collection={"allowed_countries": ["GB"]},
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 0, "currency": "gbp"},
                        "display_name": "Free shipping",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 5},
                            "maximum": {"unit": "business_day", "value": 7},
                        },
                    },
                },
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 1500, "currency": "gbp"},
                        "display_name": "Next day air",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 1},
                            "maximum": {"unit": "business_day", "value": 1},
                        },
                    },
                },
            ],
        )
        return checkout_session.url
    except Exception as e:
        raise HTTPException(403, str(e))


@app.get("/items/", response_model=List[schemas.GetItem])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


class WebHookData(BaseModel):
    data: dict
    type: str


@app.post("/webhook")
def webhook_received(
    request_data: WebHookData, stripe_signature: Optional[str] = Header(None)
):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    # request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = stripe_signature
        try:
            event = stripe.Webhook.construct_event(
                payload=request_data, sig_header=signature, secret=webhook_secret
            )
            data = event["data"]
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event["type"]
    else:
        data = request_data["data"]
        event_type = request_data["type"]
    data_object = data["object"]

    if event_type == "checkout.session.completed":
        print("🔔 Payment succeeded!")
        # Note: If you need access to the line items, for instance to
        # automate fullfillment based on the the ID of the Price, you'll
        # need to refetch the Checkout Session here, and expand the line items:
        #
        # session = stripe.checkout.Session.retrieve(
        #     data['object']['id'], expand=['line_items'])
        #
        # line_items = session.line_items
        #
        # Read more about expand here: https://stripe.com/docs/expand
    return {"status": "success"}


@app.post("/items/", response_model=schemas.CreateItem)
def create_item(item: schemas.CreateItem, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

helpers.prepopulatedb()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="127.0.0.1", port=5666)
