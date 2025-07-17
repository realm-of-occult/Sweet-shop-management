import pytest
from sweetshop.sweet_shop import Sweet, SweetShop

def make_sweet(id=1, name="Barfi", category="Milk-Based", price=10, quantity=10):
    return Sweet(id, name, category, price, quantity)

@pytest.fixture
def shop():
    return SweetShop()

def test_add_sweet(shop):
    sweet = make_sweet()
    shop.add_sweet(sweet)
    assert shop.sweets[sweet.id] == sweet

def test_add_duplicate_sweet_raises(shop):
    sweet = make_sweet()
    shop.add_sweet(sweet)
    with pytest.raises(ValueError):
        shop.add_sweet(sweet)

def test_delete_sweet(shop):
    sweet = make_sweet()
    shop.add_sweet(sweet)
    shop.delete_sweet(sweet.id)
    assert sweet.id not in shop.sweets

def test_delete_nonexistent_raises(shop):
    with pytest.raises(ValueError):
        shop.delete_sweet(99)

def test_view_sweets(shop):
    s1 = make_sweet(1)
    s2 = make_sweet(2, name="Rasgulla")
    shop.add_sweet(s1)
    shop.add_sweet(s2)
    all_sweets = shop.view_sweets()
    assert s1 in all_sweets and s2 in all_sweets

def test_search_by_name(shop):
    s1 = make_sweet(1, name="Kaju Katli")
    s2 = make_sweet(2, name="Gajar Halwa")
    shop.add_sweet(s1)
    shop.add_sweet(s2)
    res = shop.search_sweets(name="Kaju")
    assert s1 in res and s2 not in res

def test_search_by_category(shop):
    s1 = make_sweet(1, category="Nut-Based")
    s2 = make_sweet(2, category="Milk-Based")
    shop.add_sweet(s1)
    shop.add_sweet(s2)
    res = shop.search_sweets(category="Milk")
    assert s2 in res and s1 not in res

def test_search_by_price_range(shop):
    s1 = make_sweet(1, price=20)
    s2 = make_sweet(2, price=50)
    shop.add_sweet(s1); shop.add_sweet(s2)
    res = shop.search_sweets(price_min=25, price_max=60)
    assert s2 in res and s1 not in res

def test_sort_sweets(shop):
    s1 = make_sweet(1, name="Barfi")
    s2 = make_sweet(2, name="Rasgulla")
    s3 = make_sweet(3, name="Gulab Jamun")
    shop.add_sweet(s1)
    shop.add_sweet(s2)
    shop.add_sweet(s3)
    sorted_list = shop.sort_sweets(by="name")
    names = [s.name for s in sorted_list]
    assert names == sorted(names)

def test_purchase_sweet(shop):
    s1 = make_sweet(quantity=10)
    shop.add_sweet(s1)
    shop.purchase_sweet(s1.id, 3)
    assert shop.sweets[s1.id].quantity == 7

def test_purchase_more_than_stock_raises(shop):
    s1 = make_sweet(quantity=2)
    shop.add_sweet(s1)
    with pytest.raises(ValueError):
        shop.purchase_sweet(s1.id, 5)

def test_restock_sweet(shop):
    s1 = make_sweet(quantity=10)
    shop.add_sweet(s1)
    shop.restock_sweet(s1.id, 5)
    assert shop.sweets[s1.id].quantity == 15

def test_purchase_nonexistent_raises(shop):
    with pytest.raises(ValueError):
        shop.purchase_sweet(999, 1)

def test_restock_nonexistent_raises(shop):
    with pytest.raises(ValueError):
        shop.restock_sweet(999, 1)
