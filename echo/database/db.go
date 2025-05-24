package database

import (
	"go-echo-gorm-app/models"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDB() {
	var err error
	DB, err = gorm.Open(sqlite.Open("app.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect to database")
	}

	DB.AutoMigrate(
		&models.Product{},
		&models.Category{},
		&models.Customer{},
		&models.Order{},
		&models.OrderItem{},
	)
}
