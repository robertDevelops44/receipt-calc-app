INSERT INTO users (name) VALUES 
    ('Bob'),
    ('Jake'),
    ('Richard')
;

INSERT INTO items (store, name, tax, total_cost, cost_per_user) VALUES 
    ('Walmart', 'Swifter', 8, 12.99, 12.99),
    ('Walmart', 'Potatoes', 8, 6.88, 6.88),
    ('Wegmans', 'Ground Beef', 4, 23.67, 11.84)
;

INSERT INTO owners (user_id, item_id) VALUES 
    (1,3),
    (3,3)
;