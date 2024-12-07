SELECT * FROM customer;
SELECT * FROM order_item;
SELECT * FROM public.order;

DELETE FROM customer;
DELETE FROM order_item;
DELETE FROM public.order;

SELECT * FROM bag;
SELECT * FROM item;
SELECT * FROM preselection;

INSERT INTO bag (id, image_src, color, size, price) VALUES (1, '/bag1', 'blue', 'small', 10);
INSERT INTO bag (id, image_src, color, size, price) VALUES (2, '/bag2', 'yellow', 'medium', 10);

INSERT INTO item (id, image_src, title, price) VALUES (1, '/item1', 'car', 1);
INSERT INTO item (id, image_src, title, price) VALUES (2, '/item2', 'book', 1);
INSERT INTO item (id, image_src, title, price) VALUES (3, '/item3', 'candy', 1);
INSERT INTO item (id, image_src, title, price) VALUES (4, '/item4', 'sticker', 1);
INSERT INTO item (id, image_src, title, price) VALUES (5, '/item5', 'stationary', 1);

INSERT INTO preselection (id, image_src, title, price, bag_id, item_ids) VALUES (1, '/preselection1', 'preselection1', 15, 1, '{1, 2, 3}');
INSERT INTO preselection (id, image_src, title, price, bag_id, item_ids) VALUES (2, '/preselection2', 'preselection2', 16, 1, '{3, 4, 5}');
INSERT INTO preselection (id, image_src, title, price, bag_id, item_ids) VALUES (3, '/preselection3', 'preselection3', 17, 2, '{1, 2, 3}');
INSERT INTO preselection (id, image_src, title, price, bag_id, item_ids) VALUES (4, '/preselection4', 'preselection4', 18, 2, '{1, 3, 5}');