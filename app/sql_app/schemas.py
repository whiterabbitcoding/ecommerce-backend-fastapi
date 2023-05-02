from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    # id: int
    title: str
    description: str
    stock: int
    price: int
    artist: str
    # hardware: bool = False
    stripe_key: str


class ItemCreate(ItemBase):
    pass


class CartItem(ItemBase):
    pass


class CreateItem(ItemBase):
    # id: int
    title: str
    description: str
    artist: str
    price: float
    stripe_key: str
    stock: int
    product_information_url: str
    music_url: str
    image_url: str
    product_type: str
    stripe_product_ke: str

    class Config:
        orm_mode = True


class GetItem(ItemBase):
    id: int
    title: str
    description: Union[str, None]
    artist: str
    price: Union[float, str, int, None]
    stripe_key: Union[str, int, None]
    stock: int
    product_information_url: Union[str, None]
    music_url: Union[str, None]
    image_url: Union[str, None]
    product_type: Union[str, None]
    stripe_product_key: Union[str, None]

    class Config:
        orm_mode = True


class Cart(BaseModel):
    id: int
    cartitems: list

    class Config:
        orm_mode = True
