SELECT * FROM customer;
SELECT * FROM public.order;
SELECT * FROM order_item;
SELECT * FROM bag;
SELECT * FROM item;
SELECT * FROM preselection;
SELECT * FROM shipment;
SELECT * FROM shipping_method;
SELECT * FROM coupon;
SELECT * FROM inventory ORDER BY id;
SELECT * FROM inventory_transaction

DROP TABLE shipment;
DROP TABLE order_item;
DROP TABLE public.order;
DROP TABLE customer;
DROP TABLE shipment;
DROP TABLE shipping_method;
DROP TABLE inventory_transaction;
DROP TABLE inventory;
DROP TABLE coupon;
DROP TABLE preselection;
DROP TABLE item;
DROP TABLE bag;
Truncate alembic_version;

INSERT INTO bag (id, image_url, video_url, name, description, price) VALUES (1, 'https://giftoz.netlify.app/images/custom/bag1.jpeg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'bag1', 'bag1 description', 10);
INSERT INTO bag (id, image_url, video_url, name, description, price) VALUES (2, 'https://giftoz.netlify.app/images/custom/bag2.jpeg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'bag2', 'bag2 description', 15);
INSERT INTO bag (id, image_url, video_url, name, description, price) VALUES (3, 'https://giftoz.netlify.app/images/custom/bag3.jpeg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'bag3', 'bag3 description', 15);

INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (1, 'https://giftoz.netlify.app/images/custom/item1.png', 'https://www.w3schools.com/html/mov_bbb.mp4', 'sticker', 'Elsa', 'item1 description', 2);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (2, 'https://giftoz.netlify.app/images/custom/item2.jpg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'sticker', 'Batman', 'item2 description', 1);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (3, 'https://giftoz.netlify.app/images/custom/item3.jpg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'pen', 'pen1', 'item3 description', 3);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (4, 'https://giftoz.netlify.app/images/custom/item4.jpg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'pen', 'pen2', 'item4 description', 1);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (5, 'https://giftoz.netlify.app/images/custom/item5.webp', 'https://www.w3schools.com/html/mov_bbb.mp4', 'pen', 'pen3', 'item5 description', 2);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (6, 'https://giftoz.netlify.app/images/custom/item6.webp', 'https://www.w3schools.com/html/mov_bbb.mp4', 'pen', 'pen4', 'item6 description', 2);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (7, 'https://giftoz.netlify.app/images/custom/item7.webp', 'https://www.w3schools.com/html/mov_bbb.mp4', 'hairclip', 'Elsa', 'item7 description', 1);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (8, 'https://giftoz.netlify.app/images/custom/item8.jpg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'toy', 'toy1', 'item8 description', 3);
INSERT INTO item (id, image_url, video_url, product, name, description, price) VALUES (9, 'https://giftoz.netlify.app/images/custom/item9.jpg', 'https://www.w3schools.com/html/mov_bbb.mp4', 'toy', 'toy2', 'item9 description', 1);

INSERT INTO preselection (id, image_url, name, gender, description, price, bag_id, item_ids) VALUES (1, 'https://giftoz.netlify.app/images/preselections/preselection1.webp', 'preselection1', 'boys', 'Celebration Gift Pack (Person-alised)', 59, 1, '{1, 2, 3}');
INSERT INTO preselection (id, image_url, name, gender, description, price, bag_id, item_ids) VALUES (2, 'https://giftoz.netlify.app/images/preselections/preselection2.webp', 'preselection2', 'boys', 'LOL OMG Gift Pack', 109, 1, '{1, 3, 4}');
INSERT INTO preselection (id, image_url, name, gender, description, price, bag_id, item_ids) VALUES (3, 'https://giftoz.netlify.app/images/preselections/preselection3.webp', 'preselection3', 'girls', 'Fun Surprises Gift Pack', 109, 2, '{1, 2, 3}');
INSERT INTO preselection (id, image_url, name, gender, description, price, bag_id, item_ids) VALUES (4, 'https://giftoz.netlify.app/images/preselections/preselection4.png', 'preselection4', 'girls', 'Squishmallow Surprise Gift Pack', 89, 2, '{2, 3, 4}');

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

INSERT INTO coupon (code, discount_percentage, description, expiry_date, used) VALUES ('ABC123', 2, '2% discount on subtotal', '2025-10-04', false);
INSERT INTO coupon (code, discount_percentage, description, expiry_date, used) VALUES ('DEF456', 5, '5% discount on subtotal', '2025-10-04', false);
INSERT INTO coupon (code, discount_percentage, description, expiry_date, used) VALUES ('OPQ789', 10, '10% discount on subtotal', '2025-10-04', false);

INSERT INTO shipping_method (name, fee, discount_fee) VALUES ('standard', 17.95, 0);
INSERT INTO shipping_method (name, fee, discount_fee) VALUES ('express', 22.95, 9.95);
