from src.models.product_model import ProductModel
from src.models.user_model import UserModel


def db_list_product(skip, limit, db):
    products = db.query(ProductModel).offset(skip).limit(limit).all()
    return [{
        'id': product.id,
        'image': product.image,
        'description': product.description,
        'price': product.price,
        'user_id': product.user_id
    } for product in products]


def db_get_product_by_id(id, db):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        return False
    return {
        'id': product.id,
        'image': product.image,
        'description': product.description,
        'price': product.price,
        'user_id': product.user_id
    }


def db_create_product(user_id, prod_, db):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return False
    product_data = ProductModel(image=prod_.image, description=prod_.description, price=prod_.price, user_id=user_id)
    db.add(product_data)
    db.commit()

    product_inserted = db.query(ProductModel).where(ProductModel.id == product_data.id).first()
    return product_inserted


def db_update_product(id, prod_, db):
    product_data = db.query(ProductModel).filter(ProductModel.id == id).first()

    if not product_data:
        return False
    product_data.image = prod_.image
    product_data.description = prod_.description
    product_data.price = prod_.price

    db.commit()

    product_updated = db.query(ProductModel).where(ProductModel.id == id).first()
    return product_updated


def db_delete_product(id, db):
    product_data = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product_data:
        return False
    db.delete(product_data)
    db.commit()
    return product_data
