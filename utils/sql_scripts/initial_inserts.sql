SELECT * FROM customer;
SELECT * FROM public.order;
SELECT * FROM order_item;

DELETE FROM customer;
DELETE FROM public.order;

SELECT * FROM bag;
SELECT * FROM item;
SELECT * FROM preselection;
SELECT * FROM inventory ORDER BY id;

INSERT INTO bag (id, image_url, name, description, price) VALUES (1, 'https://giftoz.netlify.app/images/custom/bag1.jpeg', 'bag1', 'bag1 description', 10);
INSERT INTO bag (id, image_url, name, description, price) VALUES (2, 'https://giftoz.netlify.app/images/custom/bag2.jpeg', 'bag2', 'bag2 description', 15);
INSERT INTO bag (id, image_url, name, description, price) VALUES (3, 'https://giftoz.netlify.app/images/custom/bag3.jpeg', 'bag3', 'bag3 description', 15);

INSERT INTO item (id, image_url, name, description, price, category) VALUES (1, 'https://giftoz.netlify.app/images/custom/item1.png', 'sticker', 'item1 description', 2, 'entertainment');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (2, 'https://giftoz.netlify.app/images/custom/item2.jpg', 'sticker', 'item2 description', 1, 'entertainment');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (3, 'https://giftoz.netlify.app/images/custom/item3.jpg', 'pen', 'item3 description', 3, 'study');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (4, 'https://giftoz.netlify.app/images/custom/item4.jpg', 'pen', 'item4 description', 1, 'study');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (5, 'https://giftoz.netlify.app/images/custom/item5.webp', 'pen', 'item5 description', 2, 'study');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (6, 'https://giftoz.netlify.app/images/custom/item6.webp', 'pen', 'item6 description', 2, 'study');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (7, 'https://giftoz.netlify.app/images/custom/item7.webp', 'hairclip', 'item7 description', 1, 'dress-up');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (8, 'https://giftoz.netlify.app/images/custom/item8.jpg', 'toy', 'item8 description', 3, 'entertainment');
INSERT INTO item (id, image_url, name, description, price, category) VALUES (9, 'https://giftoz.netlify.app/images/custom/item9.jpg', 'toy', 'item9 description', 1, 'entertainment');

INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (1, 'https://giftoz.netlify.app/images/preselections/preselection1.webp', 'preselection1', 'Celebration Gift Pack (Person-alised)', 59, 1, '{1, 2, 3}');
INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (2, 'https://giftoz.netlify.app/images/preselections/preselection2.webp', 'preselection2', 'LOL OMG Gift Pack', 109, 1, '{1, 3, 4}');
INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (3, 'https://giftoz.netlify.app/images/preselections/preselection3.webp', 'preselection3', 'Fun Surprises Gift Pack', 109, 2, '{1, 2, 3}');
INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (4, 'https://giftoz.netlify.app/images/preselections/preselection4.png', 'preselection4', 'Squishmallow Surprise Gift Pack', 89, 2, '{2, 3, 4}');

INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (1, 'bag', 1, 500, 50);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (2, 'bag', 2, 500, 50);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (3, 'bag', 3, 500, 50);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (4, 'item', 1, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (5, 'item', 2, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (6, 'item', 3, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (7, 'item', 4, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (8, 'item', 5, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (9, 'item', 6, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (10, 'item', 7, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (11, 'item', 8, 100, 10);
INSERT INTO inventory (id, entity_type, entity_id, current_stock, low_stock_threshold) VALUES (12, 'item', 9, 100, 10);
