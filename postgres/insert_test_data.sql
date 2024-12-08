INSERT INTO product_categories (category_description)
VALUES 
    ('Electronics'),
    ('Home Appliances'),
    ('Clothing'),
    ('Furniture'),
    ('Sports Equipment');
INSERT INTO products (product_description, product_category)
VALUES 
    ('Smartphone', 1), -- Electronics
    ('Laptop', 1), -- Electronics
    ('Washing Machine', 2), -- Home Appliances
    ('Microwave Oven', 2), -- Home Appliances
    ('T-Shirt', 3), -- Clothing
    ('Jeans', 3), -- Clothing
    ('Sofa', 4), -- Furniture
    ('Dining Table', 4), -- Furniture
    ('Football', 5), -- Sports Equipment
    ('Tennis Racket', 5); -- Sports Equipment
INSERT INTO product_stock (product_id, quantity, measurement_unit)
VALUES 
    (1, 50, 'Units'),    -- Smartphone
    (2, 30, 'Units'),    -- Laptop
    (3, 100, 'Units'),   -- Washing Machine
    (4, 75, 'Units'),    -- Microwave Oven
    (5, 200, 'Pieces'),  -- T-Shirt
    (6, 150, 'Pieces'),  -- Jeans
    (7, 20, 'Pieces'),   -- Sofa
    (8, 10, 'Pieces'),   -- Dining Table
    (9, 500, 'Units'),   -- Football
    (10, 300, 'Units');  -- Tennis Racket