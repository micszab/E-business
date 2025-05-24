package models

import "gorm.io/gorm"

type Product struct {
	gorm.Model
	Name       string
	Price      float64
	CategoryID uint
	Category   Category
}

type Category struct {
	gorm.Model
	Name     string
	Products []Product
}

type Customer struct {
	gorm.Model
	Name  string
	Email string
}

type Order struct {
	gorm.Model
	CustomerID uint
	Customer   Customer
	OrderItems []OrderItem
}

type OrderItem struct {
	gorm.Model
	OrderID   uint
	ProductID uint
	Quantity  int
	Product   Product
}
