package controllers

import javax.inject._
import play.api.mvc._
import play.api.libs.json._
import scala.collection.mutable.ListBuffer

/**
 * Model class representing a product
 *
 * @param id Unique identifier for the product
 * @param name Product name
 * @param price Product price in dollars
 * @param category Product category
 * @param description Brief description of the product
 * @param inStock Whether the product is currently available
 */
case class Product(
  id: Int, 
  name: String, 
  price: Double,
  category: String,
  description: String = "",
  inStock: Boolean = true
)

object Product {
  // JSON formatter for Product class
  implicit val productFormat: OFormat[Product] = Json.format[Product]

  val CATEGORIES = Set("Electronics", "Clothing", "Books")
}

/**
 * Controller handling CRUD operations for products.
 */
@Singleton
class ProductController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  
  // In-memory product database
  private val products = ListBuffer(
    Product(1, "Laptop Pro", 3000.00, "Electronics", "High-performance laptop with 16GB RAM and 1TB SSD", true),
    Product(2, "Smartphone X", 1500.00, "Electronics", "Latest smartphone with 6.7-inch OLED display", true),
    Product(3, "Wireless Headphones", 250.00, "Electronics", "Noise-cancelling wireless headphones with 24h battery", true),
    Product(4, "Winter Jacket", 150.00, "Clothing", "Warm winter jacket with waterproof exterior", true),
    Product(5, "Running Shoes", 120.00, "Clothing", "Lightweight running shoes with cushioned soles", false),
    Product(6, "Cotton T-Shirt", 25.00, "Clothing", "100% cotton t-shirt in various colors", true),
    Product(7, "Programming Guide", 45.00, "Books", "Comprehensive guide to modern programming", true),
    Product(8, "Science Fiction Novel", 15.00, "Books", "Bestselling sci-fi novel about space exploration", true)
  )
  
  /**
   * @return JSON array of all products
   */
  def getAll: Action[AnyContent] = Action {
    Ok(Json.toJson(products))
      .withHeaders(CACHE_CONTROL -> "max-age=60")
  }

  /**
   * @param id The product ID to look up
   * @return JSON of the product or 404 if not found
   */
  def getById(id: Int): Action[AnyContent] = Action {
    findProductById(id) match {
      case Some(product) => Ok(Json.toJson(product))
      case None => NotFound(createErrorResponse("Product not found", "NOT_FOUND"))
    }
  }

  /**
   * @return Created status with the new product as JSON
   */
  def add: Action[JsValue] = Action(parse.json) { request =>
    request.body.validate[Product].fold(
      errors => {
        BadRequest(createErrorResponse("Invalid product data: " + JsError.toJson(errors), "VALIDATION_ERROR"))
      },
      product => {
        // Validate category
        if (!Product.CATEGORIES.contains(product.category)) {
          BadRequest(createErrorResponse(s"Invalid category. Valid categories are: ${Product.CATEGORIES.mkString(", ")}", "INVALID_CATEGORY"))
        } else {
          val newId = if (products.isEmpty) 1 else products.map(_.id).max + 1
          val newProduct = product.copy(id = newId)
          products += newProduct
          Created(Json.toJson(newProduct))
            .withHeaders("Location" -> s"/products/$newId")
        }
      }
    )
  }

  /**
   * @param id The ID of the product to update
   * @return OK with the updated product or 404 if not found
   */
  def update(id: Int): Action[JsValue] = Action(parse.json) { request =>
    request.body.validate[Product].fold(
      errors => {
        BadRequest(createErrorResponse("Invalid product data: " + JsError.toJson(errors), "VALIDATION_ERROR"))
      },
      updatedProduct => {
        // Validate category
        if (!Product.CATEGORIES.contains(updatedProduct.category)) {
          BadRequest(createErrorResponse(s"Invalid category. Valid categories are: ${Product.CATEGORIES.mkString(", ")}", "INVALID_CATEGORY"))
        } else {
          products.indexWhere(_.id == id) match {
            case -1 => NotFound(createErrorResponse("Product not found", "NOT_FOUND"))
            case index =>
              products.update(index, updatedProduct.copy(id = id))
              Ok(Json.toJson(updatedProduct.copy(id = id)))
          }
        }
      }
    )
  }

  /**
   * Delete a product by its ID.
   * 
   * @param id The ID of the product to delete
   * @return NoContent if successful or 404 if not found
   */
  def delete(id: Int): Action[AnyContent] = Action {
    products.indexWhere(_.id == id) match {
      case -1 => NotFound(createErrorResponse("Product not found", "NOT_FOUND"))
      case index =>
        products.remove(index)
        NoContent
    }
  }
  
  /**
   * @param category The category to filter by
   * @return JSON array of filtered products
   */
  def getByCategory(category: String): Action[AnyContent] = Action {
    if (!Product.CATEGORIES.contains(category)) {
      BadRequest(createErrorResponse(s"Invalid category. Valid categories are: ${Product.CATEGORIES.mkString(", ")}", "INVALID_CATEGORY"))
    } else {
      val filteredProducts = products.filter(_.category.equalsIgnoreCase(category))
      Ok(Json.toJson(filteredProducts))
    }
  }
  
  /**
   * @return JSON array of in-stock products
   */
  def getInStock: Action[AnyContent] = Action {
    val inStockProducts = products.filter(_.inStock)
    Ok(Json.toJson(inStockProducts))
  }
  
  /**
   * @param query The search query
   * @return JSON array of matching products
   */
  def search(query: String): Action[AnyContent] = Action {
    val searchResults = products.filter(p => 
      p.name.toLowerCase.contains(query.toLowerCase) || 
      p.description.toLowerCase.contains(query.toLowerCase)
    )
    Ok(Json.toJson(searchResults))
  }
  
  // Helper methods
  def findProductById(id: Int): Option[Product] = {
    products.find(_.id == id)
  }
  
  private def createErrorResponse(message: String, errorCode: String = "ERROR"): JsObject = {
    Json.obj(
      "error" -> message,
      "code" -> errorCode
    )
  }
}