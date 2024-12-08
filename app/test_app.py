import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import fakeredis, json

from main import app  
from database import get_db
from utils import get_redis

# Mock the database session dependency
mock_db = MagicMock()
app.dependency_overrides[get_db] = lambda: mock_db

# Mock Redis
redis_mock = fakeredis.FakeRedis()
app.dependency_overrides[get_redis] = lambda: redis_mock

client = TestClient(app)

# Parameterized test for category creation
@pytest.mark.parametrize(
    "category_data,expected_status,expected_message",
    [
        ({"category_description": "Valid Category"}, 200, "category Valid Category created successfully!"),
        ({"category_description": ""}, 400, "category could not be created!"),  # Invalid input
    ],
)
def test_create_category(category_data, expected_status, expected_message):
    response = client.post("/product_categories/", json=category_data)
    assert response.json()["code"] == expected_status
    assert response.json()["details"] == expected_message

# Parameterized test for deleting categories
@pytest.mark.parametrize(
    "delete_data,expected_status,expected_message",
    [
        ({"category_description": "Existing Category"}, 200, "category Existing Category deleted successfully!"),
        ({"category_description": "Non-Existing Category"}, 400, "category Non-Existing Category could not be deleted!"),
    ],
)
def test_delete_category(delete_data, expected_status, expected_message):
    if delete_data["category_description"] == "Existing Category":
        mock_db.execute.return_value.scalars().one_or_none = MagicMock(return_value=True)
    else:
        mock_db.execute.return_value.scalars().one_or_none = MagicMock(return_value=None)
    response = client.request("DELETE", "product_categories", json=delete_data)
    assert response.json()["code"] == expected_status
    assert response.json()["details"] == expected_message

# Test reading categories with Redis caching
def test_read_categories_with_redis():
    redis_key = "product_categories:0-10"
    # Populate Redis with mock data
    redis_mock.set(redis_key, '[{"category_description": "Cached Category"}]')
    
    response = client.get("/product_categories/?skip=0&limit=10")
    assert response.json()["code"] == 200
    assert response.json()["details"] == [{"category_description": "Cached Category"}]

# Test reading categories fallback to DB
def test_read_categories_fallback_to_db():
    redis_key = "product_categories:0-10"
    redis_mock.delete(redis_key)  # Ensure Redis does not contain the key

    # Mock the database query result
    mock_category_1 = MagicMock()
    mock_category_1.to_dict.return_value = {"category_description": "Category 1"}

    mock_category_2 = MagicMock()
    mock_category_2.to_dict.return_value = {"category_description": "Category 2"}

    # Mock the SQLAlchemy select result
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_category_1, mock_category_2]
    mock_db.execute.return_value = mock_result

    # Perform the request
    response = client.get("/product_categories/?skip=0&limit=10")

    # Validate the response
    assert response.json()["code"] == 200
    assert len(response.json()["details"]) == 2
    assert response.json()["details"] == [
        {"category_description": "Category 1"},
        {"category_description": "Category 2"},
    ]

# Parameterized test for creating products
@pytest.mark.parametrize(
    "product_data,expected_status,expected_message",
    [
        ({"product_description": "Product 1", "product_category":1, "price": 10.0, "quantity": 5}, 200, "product Product 1 created successfully!"),
        ({"product_description": "", "product_category": 1, "price": 10.0, "quantity": 5}, 400, "product could not be created!"),
    ],
)
def test_create_product( product_data, expected_status, expected_message):
    response = client.post("/products/", json=product_data)
    assert response.json()["code"] == expected_status
    assert response.json()["details"] == expected_message