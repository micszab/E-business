package main

import (
	"go-echo-gorm-app/controllers"
	"go-echo-gorm-app/database"

	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()
	database.InitDB()

	// Routes
	e.GET("/products", controllers.GetProducts)
	e.POST("/products", controllers.CreateProduct)
	e.GET("/products/:id", controllers.GetProduct)
	e.PUT("/products/:id", controllers.UpdateProduct)
	e.DELETE("/products/:id", controllers.DeleteProduct)

	e.Logger.Fatal(e.Start(":8080"))
}
