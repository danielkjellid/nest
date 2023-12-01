import pytest


@pytest.mark.product(name="Testing", unit="g")
@pytest.mark.products(product1={"name": "Product1"}, product2={"name": "product2"})
def test_something(*, product, products, product1, product2):
    print(product)
    print(product.name)
    print("----")
    print(products)
    print(product1.name)
    print(product2.name)
    assert False
