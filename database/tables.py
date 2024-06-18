from typing import List
from sqlalchemy import String, Numeric, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ipn: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(150), nullable=True)

    account_balance: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    last_activity: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    detected_fraudster: Mapped[bool] = mapped_column(Boolean, default=False)

    transactions = relationship(
        "Transaction",
        primaryjoin="or_(User.id == Transaction.sender_id, User.id == Transaction.receiver_id)",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    transaction_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    transaction_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    transaction_category: Mapped[str] = mapped_column(String(150), nullable=False)

    user = relationship(
        "User",
        primaryjoin="or_(Transaction.sender_id == User.id, Transaction.receiver_id == User.id)",
        back_populates="transactions",
        uselist=True
    )


list_categories = ["Groceries", "Restaurants and Cafes", "Fuel and Auto Parts", "Travel and Hotels",
                   "Entertainment and Cinemas", "Fashion and Clothing", "Electronics and Gadgets",
                   "Furniture and Home Decor", "Pharmacies and Medical Services", "Online Stores",
                   "Sporting Goods and Fitness", "Cosmetics and Personal Care", "Communication and Internet Services",
                   "Children's Products and Toys", "Banking Services", "Auto Services", "Books and Stationery",
                   "Building Materials", "Jewelry and Accessories", "Flowers and Gifts", "Personal Transfer"]
