CREATE TABLE IF NOT EXISTS
    product_categories ( 
        id SERIAL PRIMARY KEY,
        category_description VARCHAR(200) NOT NULL
    );
CREATE TABLE IF NOT EXISTS
    products ( 
        id SERIAL PRIMARY KEY,
        product_description VARCHAR(200) NOT NULL,
        product_category INTEGER NOT NULL,
        FOREIGN KEY
            (product_category)
        REFERENCES
            product_categories(id)
        ON DELETE CASCADE 
    );
CREATE TABLE IF NOT EXISTS
    product_stock ( 
        id SERIAL PRIMARY KEY,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        measurement_unit VARCHAR(200),
        FOREIGN KEY
            (product_id)
        REFERENCES
            products(id)
        ON DELETE CASCADE 
    );

-- CUSTOM PLPGSQL FUNCTION THAT SENDS MESSAGE WITH RELEVENT DATA TO A SPECIFIC TOPIC 

CREATE OR REPLACE FUNCTION notify_cache_invalidation()
RETURNS trigger AS $$
DECLARE
    payload json;
BEGIN
    -- Construct a payload with relevant data
    payload = json_build_object(
        'table', TG_TABLE_NAME,
        'operation', TG_OP,
        'key', NEW.id -- Assume the primary key is 'id'
    );

    -- Publish using the `pg_notify` function
    PERFORM pg_notify('cache_invalidation', payload::text);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- CREATE TRIGGERS FOR OUR TABLES, TO SEND MESSAGE WHEN A WRITE (INSERT, UPDATE, DELETE) OPERATION TOOK PLACE

CREATE TRIGGER invalidate_cache
AFTER INSERT OR UPDATE OR DELETE ON product_categories
FOR EACH ROW EXECUTE FUNCTION notify_cache_invalidation();

CREATE TRIGGER invalidate_cache
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION notify_cache_invalidation();

CREATE TRIGGER invalidate_cache
AFTER INSERT OR UPDATE OR DELETE ON product_stock
FOR EACH ROW EXECUTE FUNCTION notify_cache_invalidation();