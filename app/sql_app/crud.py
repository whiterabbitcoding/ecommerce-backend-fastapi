from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    print(db.query(models.Item).offset(skip).limit(limit).all())
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, id: id):
    item = db.query(models.Item).get(id).__dict__
    print("item")

    print(item)
    return db.query(models.Item).get(id).__dict__


def get_cart(db: Session, id: id):
    print(dir(db.query(models.Cart).get(id)))
    query = db.query(models.Cart).get(id)
    output = {"cartitems": query.cartitems, "id": query.id}
    print("output")
    print(output)
    return db.query(models.Cart).get(id)


# def get_display_cart(db: Session, id: id)
#     cart = get_cart(id)
#     cart_items = [ cart_item.__dict__ for cart_item in cart.cartitems]
#     new_cart =
#     for cart_item in cart_items:
#         item = get_item(cart_item.item_id)
#         new_cart_item = {cart_item[k] = v for (k,v) in item }


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    print(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_cart_item(db: Session, cart_id, item_id):
    item = db.query(models.Item).get(cart_id)
    cart = db.query(models.Cart).get(item_id)
    db_item = models.CartItem(
        item=db.query(models.Item).get(item_id),
        cart=db.query(models.Cart).get(cart_id),
        quantity=1,
    )
    print(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_cart(
    db: Session,
    # cart,
    item_id,
):
    # db_item = models.Cart(**cart.dict())
    # db_item = models.Cart(items=[db.query(models.Item).get(item_id)])
    cart = models.Cart(cartitems=[])
    print(cart)
    db.add(cart)
    # db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def add_to_cart(db: Session, cart_id, item_id, remove=False):
    # def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    print("herro")
    cart = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).first()

    print("cart")
    print(cart)
    print("cartid")
    print(cart_id)
    print("item_id")
    print(item_id)
    cart_item_result = db.query(models.CartItem).filter(
        models.CartItem.cart_id.like(cart_id),
        models.CartItem.item_id.like(item_id),
    )
    print("first")
    print(cart_item_result.first())
    cart_item = cart_item_result.first()
    print("cart_item")
    print(cart_item)

    if remove:
        cart_item.quantity -= 1
        if cart_item.quantity == 0:
            db.delete(cart_item)
    else:
        if cart_item == None:
            print("no cart item")
            cart_item = models.CartItem(
                item=db.query(models.Item).get(item_id),
                cart=db.query(models.Cart).get(cart_id),
                quantity=1,
            )
            print(cart_item)
            print("quantity")
            print(cart_item.quantity)
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
        else:
            print(cart_item.quantity)
            if cart_item.quantity == None:
                cart_item.quantity = 1
            cart_item.quantity += 1

    item = db.query(models.Item).get(item_id)
    cart = db.query(models.Cart).get(cart_id)
    print("cart")
    print(cart)
    db.commit()
    return cart


def add_to_cart_new(db: Session, cart_id, item_id):
    cart_item = create_cart_item(db, cart_id, item_id)
    cart = db.query(models.Cart).get(cart_id)
    return cart


def remove_from_cart(db: Session, cart_id, item_id):
    pass
