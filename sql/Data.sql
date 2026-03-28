USE CuratedBites;

INSERT INTO Users (UserID, Username, Email, Password, GoogleID, CreationDate, ProfilePhoto) VALUES
(1, 'foodAddict', 'marcus123@gmail.com', SHA2('x7Kp$2qLm9Wz', 256), NULL, '2025-01-14', NULL),
(2, 'IloveFood123', 'tyler5@outlook.com', SHA2('SDFG5xcfgdf', 256), NULL, '2026-01-05', NULL),
(3, 'JohhnyBoy', 'Jonny@gmail.com', SHA2('234sd5fFDSgsdf4', 256), NULL, '2024-05-15', NULL),
(4, 'Bobby', 'Bob123@hotmail.com', SHA2('IloveFood1235', 256), NULL, '2026-03-02', NULL),
(5, 'Sonny', 'SonnyHayes@gmail.com', SHA2('Formula1IsCool123', 256), NULL, '2025-12-18', NULL);

INSERT INTO Restaurant (RestaurantID, Name, Address, City, Phone, Website, Description, Hours, PriceRange) VALUES
(1, 'Taco Bell', '1234 Food Drive', 'Irvine', '555-555-5555', 'Tacobell.com', 'Fast food dining', 'Mon-Sun 10AM-10PM', 1),
(2, 'Taco Stand', '1111 Beach Drive', 'San Diego', '555-252-7474', 'TacoStand.com', 'Food Stand', 'Mon-Sun 12PM-11PM', 2),
(3, 'Canes', '1111 Food Drive', 'Los Angeles', '555-141-2442', 'Canes.com', 'Fast Food ', 'Mon-Sun 10AM-11PM', 1),
(4, 'Deli News', '1212 Food Drive', 'Long Beach', '555-333-4444', 'DeliNews.com', 'Fast Food', 'Mon-Sun 11AM-8PM', 3),
(5, 'Fogo De Chao', '3124 Food Drive', 'Costa Mesa', '555-111-2222', 'FogoDeChao.com', 'Steakhouse', 'Mon-Sun 10AM-10PM', 4),
(6, 'McDonalds', '1235 Food Drive', 'Irvine', '555-555-1111', 'McDonalds.com', 'Fast Food', 'Mon-Sun 12AM-12PM', 1);

INSERT INTO Cuisine (CuisineID, Name) VALUES
(1, 'Italian'),
(2, 'Japanese'),
(3, 'Vegan'),
(4, 'Mexican'),
(5, 'French'),
(6, 'Indian'),
(7, 'American');

INSERT INTO Diet (DietaryOptionID, Name) VALUES
(1, 'Vegan'),
(2, 'Vegetarian'),
(3, 'Gluten-Free'),
(4, 'Nut-Free'),
(5, 'Dairy-Free');

INSERT INTO RestaurantCuisine (RestaurantID, CuisineID) VALUES
(1, 4),
(1, 7),
(2, 4),
(3, 7),
(4, 7),
(4, 1),
(5, 7),
(6, 7);

INSERT INTO RestaurantDiet (RestaurantID, DietaryOptionID) VALUES
(1, 2),
(1, 5),
(2, 3),
(2, 5),
(3, 3),
(4, 2),
(4, 3),
(5, 3),
(5, 5),
(6, 2),
(6, 5);

INSERT INTO Menu (MenuItemID, RestaurantID, Name, Description, Price, Category) VALUES
(1, 1, 'Crunchwrap Supreme', 'Seasoned beef, nacho cheese, lettuce', 4.99, 'Entree'),
(2, 1, 'Cheesy Gordita Crunch', 'Beef, three-cheese blend, gordita shell', 5.49, 'Entree'),
(3, 1, 'Baja Blast Freeze', 'Frozen tropical lime drink', 2.99, 'Beverage'),
(4, 2, 'Fish Tacos (2)', 'Grilled fish, cabbage slaw, chipotle', 9.50, 'Entree'),
(5, 2, 'Carne Asada Fries', 'Fries topped with steak and guac', 11.00, 'Entree'),
(6, 3, 'Box Combo', 'Chicken fingers, fries, toast, coleslaw', 8.99, 'Entree'),
(7, 3, 'Extra Chicken Fingers', 'Three additional chicken fingers', 3.49, 'Side'),
(8, 4, 'Pastrami Sandwich', 'Hot pastrami on rye with mustard', 12.99, 'Entree'),
(9, 4, 'Greek Salad', 'Romaine, feta, olives, cucumber', 9.50, 'Appetizer'),
(10, 4, 'Pepperoni Pizza', 'Mozzarella, pepperoni, marinara sauce', 11.99, 'Entree'),
(11, 4, 'Margherita Pizza', 'Fresh mozzarella, basil, tomato sauce', 10.99, 'Entree'),
(12, 5, 'Picanha', 'Brazilian top sirloin, carved tableside', 64.95, 'Entree'),
(13, 5, 'Lamb Chops', 'Seasoned lamb, fire-roasted', 64.95, 'Entree'),
(14, 5, 'Brazilian Cheesecake', 'Creamy dulce de leche cheesecake', 12.00, 'Dessert'),
(15, 6, 'Big Mac', 'Two beef patties, special sauce, lettuce', 5.99, 'Entree'),
(16, 6, 'McChicken', 'Crispy chicken patty, mayo, lettuce', 3.49, 'Entree');

INSERT INTO Review (ReviewID, UserID, RestaurantID, Rating, Description, ReviewDate, ReviewRatingCounter) VALUES
(1, 1, 1, 4, 'Solid late night option. Crunchwrap never fails.', '2025-02-10', 2),
(2, 2, 1, 3, 'Its Taco Bell. You know what you are getting.', '2026-01-20', 1),
(3, 3, 2, 5, 'Best fish tacos in San Diego hands down.', '2024-06-01', 5),
(4, 4, 2, 4, 'Fresh ingredients and great vibes.', '2026-03-05', 3),
(5, 5, 3, 5, 'The chicken is always so crispy and fresh.', '2025-12-20', 4),
(6, 1, 3, 4, 'Simple menu but they do it perfectly.', '2025-03-15', 2),
(7, 2, 4, 4, 'Huge portions and great pastrami.', '2026-02-01', 1),
(8, 3, 5, 5, 'Best steakhouse experience I have ever had.', '2024-08-10', 6),
(9, 4, 5, 5, 'Endless meat carved at the table. Incredible.', '2026-03-10', 3),
(10, 5, 6, 3, 'Quick and cheap but nothing special.', '2026-01-05', 0),
(11, 1, 6, 2, 'Fries were cold. Not a great visit.', '2025-04-20', 1),
(12, 3, 4, 4, 'The margherita pizza is comfort food at its finest.', '2024-09-30', 2);

INSERT INTO Favorite (FavoriteID, UserID, RestaurantID) VALUES
(1, 1, 1),
(2, 1, 3),
(3, 2, 4),
(4, 3, 2),
(5, 3, 5),
(6, 4, 5),
(7, 5, 3);