USE CuratedBites;

-- Checking restaurant by cuisine type searching for specific type
SELECT r.Name AS Restaurant, r.City, r.PriceRange, c.Name AS Cuisine
FROM Restaurant r
JOIN RestaurantCuisine rc ON r.RestaurantID = rc.RestaurantID
JOIN Cuisine c ON rc.CuisineID = c.CuisineID
WHERE c.Name = 'Mexican';

-- Finding restaurant within users budget/price range
SELECT r.Name AS Restaurant, r.City, c.Name AS Cuisine, r.PriceRange
FROM Restaurant r
JOIN RestaurantCuisine rc ON r.RestaurantID = rc.RestaurantID
JOIN Cuisine c ON rc.CuisineID = c.CuisineID
WHERE r.PriceRange <= 2
ORDER BY r.PriceRange ASC;

-- Filtering based of dietary accommodations (example is gluten-free)
SELECT r.Name AS Restaurant, r.City, d.Name AS DietaryOption
FROM Restaurant r
JOIN RestaurantDiet rd ON r.RestaurantID = rd.RestaurantID
JOIN Diet d ON rd.DietaryOptionID = d.DietaryOptionID
WHERE d.Name = 'Gluten-Free';

-- Viewing avg rating for each restaurant
SELECT r.Name AS Restaurant, ROUND(AVG(rv.Rating), 2) AS AvgRating,
       COUNT(rv.ReviewID) AS TotalReviews
FROM Restaurant r RIGHT JOIN Review rv ON r.RestaurantId = rv.RestaurantID
GROUP BY r.RestaurantID, r.Name ORDER BY AvgRating DESC;

-- View all reviews for particular restaurant (example is taco bell)
SELECT u.Username, rv.Rating, rv.Description AS ReviewText, rv.ReviewDate
FROM Review rv JOIN Users u ON rv.UserID = u.UserID
JOIN Restaurant r ON rv.RestaurantID = r.RestaurantID
WHERE r.Name = 'Taco Bell' ORDER BY rv.ReviewDate DESC;

-- Viewing menu items with different prices
SELECT r.Name AS Restaurant, m.Name AS MenuItem, m.Price, m.Category,
CASE
    WHEN m.Price < 5 THEN 'Budget'
    WHEN m.Price < 15 THEN 'Average'
    ELSE 'Premium'
END  AS PriceTier FROM Menu m
JOIN Restaurant r ON m.RestaurantID = r.RestaurantID
WHERE r.RestaurantID IN (SELECT RestaurantID FROM Review GROUP BY RestaurantID HAVING COUNT(ReviewID) >= 2)
ORDER BY r.Name, m.Price;

-- Listing each user's favorite restaurant with cuisine
SELECT u.Username, r.Name AS Restaurant, r.City, c.Name AS Cuisine FROM Favorite f
JOIN Users u ON f.UserID = u.UserID
JOIN Restaurant r ON f.RestaurantID = r.RestaurantID
JOIN RestaurantCuisine rc ON r.RestaurantID = rc.RestaurantID
JOIN Cuisine c ON rc.CuisineID = c.CuisineID ORDER BY u.Username, r.Name;

-- Search restaurant by city
SELECT r.City, COUNT(DISTINCT r.RestaurantID) AS NumRestaurants,
       ROUND(AVG(rv.Rating), 2) AS AvgCityRating
FROM Restaurant r LEFT JOIN Review rv ON r.RestaurantID = rv.RestaurantID
GROUP BY r.City ORDER BY NumRestaurants DESC;

-- Transaction Example

START TRANSACTION;

INSERT INTO Review(ReviewID, UserID, RestaurantID, Rating, Description, ReviewDate, ReviewRatingCounter)
-- Having user 4/bobby write review for canes
VALUES (13, 4, 3, 5, 'These are the best chicken fingers I''ve had in years and it was perfectly crisp.', '2026-03-02', 0);
-- Adding canes as a favorite
INSERT INTO Favorite ( UserID, RestaurantID)
VALUES (4, 3);

COMMIT;
