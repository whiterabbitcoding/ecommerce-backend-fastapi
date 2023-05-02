from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase


# from .database import Base


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    # id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    artist = Column(String, index=True)
    price = Column(String, index=True)
    stripe_key = Column(String, index=True)
    stock = Column(Integer, index=True)
    product_information_url = Column(String, index=True)
    music_url = Column(String, index=True)
    image_url = Column(String, index=True)
    # """Make multichoice?"""
    product_type = Column(String, index=True)
    stripe_product_key = Column(String, index=True)
    # hardware = Column(Boolean, index=True)
    cartitems: Mapped[List["CartItem"]] = relationship(back_populates="item")


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    cartitems: Mapped[List["CartItem"]] = relationship(back_populates="cart")


class CartItem(Base):
    __tablename__ = "cartitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    cart: Mapped["Cart"] = relationship("Cart", back_populates="cartitems")
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item: Mapped["Item"] = relationship("Item", back_populates="cartitems")
    # name: Mapped[str] = mapped_column("items.title")
    quantity: int = Column(
        Integer,
        index=True,
    )
