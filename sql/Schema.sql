CREATE DATABASE CuratedBites;
USE CuratedBites;

CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    GoogleID VARCHAR(255) DEFAULT NULL,
    CreationDate DATE NOT NULL DEFAULT(CURRENT_DATE),
    ProfilePhoto VARCHAR(255) DEFAULT NULL
);

CREATE TABLE Restaurant (
    RestaurantID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(200) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Website VARCHAR(255),
    Description TEXT,
    Hours VARCHAR(255),
    PriceRange INT NOT NULL CHECK (PriceRange BETWEEN 1 AND 4)
);

CREATE TABLE Cuisine (
    CuisineID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Diet (
    DietaryOptionID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Menu (
    MenuItemID INT PRIMARY KEY AUTO_INCREMENT,
    RestaurantID INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    Price DECIMAL(8,2) NOT NULL CHECK (Price > 0),
    Category VARCHAR(50),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

CREATE TABLE Review (
    ReviewID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    RestaurantID INT NOT NULL,
    Rating INT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    Description TEXT,
    ReviewDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    ReviewRatingCounter INT DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

CREATE TABLE Favorite (
    FavoriteID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    RestaurantID INT NOT NULL,
    UNIQUE (UserID, RestaurantID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

CREATE TABLE RestaurantCuisine (
    RestaurantID INT NOT NULL,
    CuisineID INT NOT NULL,
    PRIMARY KEY (RestaurantID, CuisineID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID),
    FOREIGN KEY (CuisineID) REFERENCES Cuisine(CuisineID)
);

CREATE TABLE RestaurantDiet (
    RestaurantID INT NOT NULL,
    DietaryOptionID INT NOT NULL,
    PRIMARY KEY (RestaurantID, DietaryOptionID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID),
    FOREIGN KEY (DietaryOptionID) REFERENCES Diet(DietaryOptionID)
);

CREATE INDEX idxReviewRestaurant ON Review(RestaurantID);
CREATE INDEX idxFavoriteUser ON Favorite(UserID);

CREATE OR REPLACE VIEW RestaurantSummary AS
SELECT
    r.RestaurantID,
    r.Name,
    r.City,
    r.PriceRange,
    GROUP_CONCAT(DISTINCT c.Name ORDER BY c.Name SEPARATOR ', ') AS Cuisines,
    COUNT(DISTINCT rv.ReviewID) AS ReviewCount,
    ROUND(AVG(rv.Rating), 2) AS AvgRating,
    COUNT(DISTINCT f.FavoriteID) AS FavoriteCount
FROM Restaurant r
LEFT JOIN RestaurantCuisine rc ON r.RestaurantID = rc.RestaurantID
LEFT JOIN Cuisine c ON rc.CuisineID = c.CuisineID
LEFT JOIN Review rv ON r.RestaurantID = rv.RestaurantID
LEFT JOIN Favorite f ON r.RestaurantID = f.RestaurantID
GROUP BY r.RestaurantID, r.Name, r.City, r.PriceRange;