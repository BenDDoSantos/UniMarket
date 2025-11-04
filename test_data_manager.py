#!/usr/bin/env python3
"""
Critical-path testing script for data_manager JSON persistence functionality.
Tests basic load/save operations for users, products, and categories.
"""

import json
import os
from data_manager import data_manager

def test_data_loading():
    """Test loading data from JSON files"""
    print("Testing data loading...")

    # Test users loading
    users = data_manager.users
    print(f"Loaded {len(users)} users")
    assert len(users) > 0, "No users loaded"

    # Test products loading
    products = data_manager.products
    print(f"Loaded {len(products)} products")
    assert len(products) > 0, "No products loaded"

    # Test categories loading
    categories = data_manager.categories
    print(f"Loaded {len(categories)} categories")
    assert len(categories) > 0, "No categories loaded"

    print("✓ Data loading tests passed")

def test_data_saving():
    """Test saving data to JSON files"""
    print("Testing data saving...")

    # Test adding a new user
    initial_users = len(data_manager.users)
    new_user = {
        'email': 'test@example.com',
        'password': 'testpass',
        'name': 'Test User'
    }
    data_manager.register_user(new_user['email'], new_user['password'], new_user['name'])
    updated_users = len(data_manager.users)
    assert updated_users == initial_users + 1, "User not added"
    print("✓ User saving test passed")

    # Test adding a new product
    initial_products = len(data_manager.products)
    new_product = {
        'nombre': 'Test Product',
        'precio': 100,
        'descripcion': 'Test description',
        'imagen': 'test.jpg'
    }
    data_manager.add_product(new_product)
    updated_products = len(data_manager.products)
    assert updated_products == initial_products + 1, "Product not added"
    print("✓ Product saving test passed")

    # Test updating a product
    if data_manager.products:
        product_id = data_manager.products[-1]['id']  # Last added product
        update_data = {'estado': 'Vendido'}
        data_manager.update_product(product_id, update_data)
        assert data_manager.products[-1]['estado'] == 'Vendido', "Product not updated"
        print("✓ Product update test passed")

def test_user_session():
    """Test user session tracking"""
    print("Testing user session...")

    # Simulate login
    test_user = data_manager.users[0] if data_manager.users else None
    if test_user:
        data_manager.current_user = test_user
        assert data_manager.current_user == test_user, "Current user not set"
        print("✓ User session test passed")
    else:
        print("⚠ No users available for session test")

def test_persistence():
    """Test data persistence by reloading data_manager"""
    print("Testing persistence...")

    # Reload data_manager to simulate app restart
    data_manager.__init__()  # Reinitialize

    # Check if data persists
    users = data_manager.users
    products = data_manager.products
    categories = data_manager.categories

    assert len(users) > 0, "Users not persisted"
    assert len(products) > 0, "Products not persisted"
    assert len(categories) > 0, "Categories not persisted"

    print("✓ Persistence test passed")

def cleanup_test_data():
    """Remove test data added during testing"""
    print("Cleaning up test data...")

    # Remove test user
    data_manager.users = [u for u in data_manager.users if u['email'] != 'test@example.com']
    data_manager.save_json(data_manager.users_file, data_manager.users)

    # Remove test product
    data_manager.products = [p for p in data_manager.products if p['nombre'] != 'Test Product']
    data_manager.save_json(data_manager.products_file, data_manager.products)

    print("✓ Test data cleaned up")

if __name__ == "__main__":
    try:
        test_data_loading()
        test_data_saving()
        test_user_session()
        test_persistence()
        cleanup_test_data()
        print("\n🎉 All critical-path tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
