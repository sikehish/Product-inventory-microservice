import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv

load_dotenv()

REDIS_PW=os.environ.get("REDIS_CLOUD_PW")

app = FastAPI()

app.add_middleware(CORSMiddleware )

redis= get_redis_connection(
    host="redis-17582.c301.ap-south-1-1.ec2.cloud.redislabs.com",
    port="17582",
    password="rGSkMqeycAbuutWEuQULlNdWuxC8vRj1",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database=redis
    

@app.get("/products")
def all():
    arr=[]
    for pk in Product.all_pks():
        arr.push(format(pk))
    return arr
    # OR return [format(pk) for pk in Product.all_pks()]


@app.post("/products")
def create(product: Product):
    print(product, type(product))
    return product.save()

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name' : product.name,
        'price': product.price,
        'quantity': product.quantity
    }

