# Relational Schema
The primary keys are **bolded**, foreign keys are *italicized*. Columns marked PK/FK are both. Types and constraints reflect the final `sql/Schema.sql`.

## Users
Users (**UserID**, Username, Email, Password, GoogleID, CreationDate, ProfilePhoto)

| Column | Type | Constraints |
|---|---|---|
| **UserID** | INT | PRIMARY KEY, AUTO_INCREMENT |
| Username | VARCHAR(50) | NOT NULL, UNIQUE |
| Email | VARCHAR(100) | NOT NULL, UNIQUE |
| Password | VARCHAR(255) | NOT NULL (stored as SHA2-256 hash) |
| GoogleID | VARCHAR(255) | DEFAULT NULL |
| CreationDate | DATE | NOT NULL, DEFAULT CURRENT_DATE |
| ProfilePhoto | VARCHAR(255) | DEFAULT NULL |

## Restaurant
Restaurant (**RestaurantID**, Name, Address, City, Phone, Website, Description, Hours, PriceRange)

| Column | Type | Constraints |
|---|---|---|
| **RestaurantID** | INT | PRIMARY KEY, AUTO_INCREMENT |
| Name | VARCHAR(100) | NOT NULL |
| Address | VARCHAR(200) | NOT NULL |
| City | VARCHAR(100) | NOT NULL |
| Phone | VARCHAR(20) | NOT NULL |
| Website | VARCHAR(255) | NULL allowed |
| Description | TEXT | NULL allowed |
| Hours | VARCHAR(255) | NULL allowed |
| PriceRange | INT | NOT NULL, CHECK (PriceRange BETWEEN 1 AND 4) |

## Cuisine
Cuisine (**CuisineID**, Name)

| Column | Type | Constraints |
|---|---|---|
| **CuisineID** | INT | PRIMARY KEY, AUTO_INCREMENT |
| Name | VARCHAR(50) | NOT NULL, UNIQUE |

## Diet
Diet (**DietaryOptionID**, Name)

| Column | Type | Constraints |
|---|---|---|
| **DietaryOptionID** | INT | PRIMARY KEY, AUTO_INCREMENT |
| Name | VARCHAR(50) | NOT NULL, UNIQUE |

## Menu
Menu (**MenuItemID**, *RestaurantID*, Name, Description, Price, Category)

| Column | Type | Constraints |
|---|---|---|
| **MenuItemID** | INT | PRIMARY KEY, AUTO_INCREMENT |
| *RestaurantID* | INT | NOT NULL, FOREIGN KEY → Restaurant(RestaurantID) |
| Name | VARCHAR(100) | NOT NULL |
| Description | TEXT | NULL allowed |
| Price | DECIMAL(8,2) | NOT NULL, CHECK (Price > 0) |
| Category | VARCHAR(50) | NULL allowed |

## Review
Review (**ReviewID**, *UserID*, *RestaurantID*, Rating, Description, ReviewDate, ReviewRatingCounter)

| Column | Type | Constraints |
|---|---|---|
| **ReviewID** | INT | PRIMARY KEY, AUTO_INCREMENT |
| *UserID* | INT | NOT NULL, FOREIGN KEY → Users(UserID) |
| *RestaurantID* | INT | NOT NULL, FOREIGN KEY → Restaurant(RestaurantID) |
| Rating | INT | NOT NULL, CHECK (Rating BETWEEN 1 AND 5) |
| Description | TEXT | NULL allowed |
| ReviewDate | DATE | NOT NULL, DEFAULT CURRENT_DATE |
| ReviewRatingCounter | INT | DEFAULT 0 |

Index: `idxReviewRestaurant` on Review(*RestaurantID*) speeds up each restaurant review lookups and the `RestaurantSummary` view.

## Favorite
Favorite (**FavoriteID**, *UserID*, *RestaurantID*)

| Column | Type | Constraints |
|---|---|---|
| **FavoriteID** | INT | PRIMARY KEY, AUTO_INCREMENT |
| *UserID* | INT | NOT NULL, FOREIGN KEY → Users(UserID) |
| *RestaurantID* | INT | NOT NULL, FOREIGN KEY → Restaurant(RestaurantID) |

Table-level constraint: UNIQUE (*UserID*, *RestaurantID*) — a user can only favorite a given restaurant once.

Index: `idxFavoriteUser` on Favorite(*UserID*) speeds up the `/api/users/<id>/favorites` endpoint.

## RestaurantCuisine

RestaurantCuisine (***RestaurantID***, ***CuisineID***)

| Column | Type | Constraints |
|---|---|---|
| ***RestaurantID*** | INT | NOT NULL, PRIMARY KEY (composite), FOREIGN KEY → Restaurant(RestaurantID) |
| ***CuisineID*** | INT | NOT NULL, PRIMARY KEY (composite), FOREIGN KEY → Cuisine(CuisineID) |

Junction table resolving the many-to-many relationship between Restaurant and Cuisine.

## RestaurantDiet

RestaurantDiet (***RestaurantID***, ***DietaryOptionID***)

| Column | Type | Constraints |
|---|---|---|
| ***RestaurantID*** | INT | NOT NULL, PRIMARY KEY (composite), FOREIGN KEY → Restaurant(RestaurantID) |
| ***DietaryOptionID*** | INT | NOT NULL, PRIMARY KEY (composite), FOREIGN KEY → Diet(DietaryOptionID) |

Junction table resolving the many-to-many relationship between Restaurant and Diet.

## DB Object - RestaurantSummary | View

A read-only view that aggregates per-restaurant analytics for use by `/api/insights/restaurants/summary`.

Columns: RestaurantID, Name, City, PriceRange, Cuisines (concatenated), ReviewCount, AvgRating, FavoriteCount.

Source tables: Restaurant LEFT JOIN RestaurantCuisine LEFT JOIN Cuisine LEFT JOIN Review LEFT JOIN Favorite, grouped by RestaurantID. LEFT JOINs ensure restaurants with no reviews or favorites still appear (with NULL/0 counts).

## Summary of the Relationships

- Users | 1 to many | Review (from *UserID*)
- Users | 1 to many | Favorite (form *UserID*)
- Restaurant | 1 to many | Review (from *RestaurantID*)
- Restaurant | 1 to many | Favorite (from *RestaurantID*)
- Restaurant | 1 to many | Menu (from *RestaurantID*)
- Restaurant | many to many | Cuisine (from RestaurantCuisine)
- Restaurant | many to many | Diet (from RestaurantDiet)
