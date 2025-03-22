package controllers

import javax.inject._
import play.api.mvc._
import play.api.libs.json._
import scala.collection.mutable.{ListBuffer, Map => MutableMap}

/**
 * Model class representing a cart item
 *
 * @param productId ID of the product in the cart
 * @param quantity Number of items
 * @param price Price of the product
 */
case class CartItem(
  productId: Int,
  quantity: Int,
  price: Double
)

/**
 * Model class representing a shopping cart
 *
 * @param id Unique identifier for the cart
 * @param items List of items in the cart
 * @param createdAt Timestamp when the cart was created
 */
case class Cart(
  id: String,
  items: List[CartItem],
  createdAt: Long = System.currentTimeMillis()
)

object CartItem {
  // JSON formatter for CartItem class
  implicit val cartItemFormat: OFormat[CartItem] = Json.format[CartItem]
}

object Cart {
  // JSON formatter for Cart class
  implicit val cartFormat: OFormat[Cart] = Json.format[Cart]
}

/**
 * Controller handling CRUD operations for shopping carts.
 */
@Singleton
class CartController @Inject()(
  val controllerComponents: ControllerComponents,
  productController: ProductController
) extends BaseController {
  
  // In-memory cart database
  private val carts: MutableMap[String, Cart] = MutableMap.empty
  
  /**
   * @param id The cart ID to look up
   * @return JSON of the cart or 404 if not found
   */
  def getById(id: String): Action[AnyContent] = Action {
    carts.get(id) match {
      case Some(cart) => Ok(Json.toJson(cart))
      case None => NotFound(createErrorResponse("Cart not found", "NOT_FOUND"))
    }
  }
  
  /**
   * Creates a new empty shopping cart
   * @return Created status with the new cart as JSON
   */
  def create: Action[AnyContent] = Action {
    val cartId = java.util.UUID.randomUUID().toString
    val newCart = Cart(cartId, List.empty)
    carts.put(cartId, newCart)
    Created(Json.toJson(newCart))
      .withHeaders("Location" -> s"/carts/$cartId")
  }
  
  /**
   * Adds an item to a cart or updates quantity if already exists
   * 
   * @param id The cart ID
   * @return OK with the updated cart or error if cart/product not found
   */
  def addItem(id: String): Action[JsValue] = Action(parse.json) { request =>
    request.body.validate[CartItem].fold(
      errors => {
        BadRequest(createErrorResponse("Invalid cart item data: " + JsError.toJson(errors), "VALIDATION_ERROR"))
      },
      item => {
        carts.get(id) match {
          case None => 
            NotFound(createErrorResponse("Cart not found", "NOT_FOUND"))
          case Some(cart) => 
            processAddItemToCart(cart, item, id)
        }
      }
    )
  }
  
  /**
   * Removes an item from a cart
   * 
   * @param id The cart ID
   * @param productId The product ID to remove
   * @return OK with the updated cart or error if cart/product not found
   */
  def removeItem(id: String, productId: Int): Action[AnyContent] = Action {
    carts.get(id) match {
      case None => 
        NotFound(createErrorResponse("Cart not found", "NOT_FOUND"))
      case Some(cart) =>
        if (!cart.items.exists(_.productId == productId)) {
          BadRequest(createErrorResponse("Product not in cart", "PRODUCT_NOT_IN_CART"))
        } else {
          val updatedItems = cart.items.filterNot(_.productId == productId)
          val updatedCart = cart.copy(items = updatedItems)
          carts.update(id, updatedCart)
          Ok(Json.toJson(updatedCart))
        }
    }
  }
  
  /**
   * Get all carts (for admin purposes)
   * @return JSON array of all carts
   */
  def getAll: Action[AnyContent] = Action {
    Ok(Json.toJson(carts.values.toList))
  }
  
  /**
   * Clear all items from a cart
   * 
   * @param id The cart ID to clear
   * @return OK with the empty cart or error if cart not found
   */
  def clearCart(id: String): Action[AnyContent] = Action {
    carts.get(id) match {
      case None => 
        NotFound(createErrorResponse("Cart not found", "NOT_FOUND"))
      case Some(cart) =>
        val updatedCart = cart.copy(items = List.empty)
        carts.update(id, updatedCart)
        Ok(Json.toJson(updatedCart))
    }
  }
  
  // Helper methods
  
  /**
   * Process adding an item to a cart, checking product validity
   */
  private def processAddItemToCart(cart: Cart, item: CartItem, cartId: String): Result = {
    productController.findProductById(item.productId) match {
      case None => 
        BadRequest(createErrorResponse("Product not found", "INVALID_PRODUCT"))
      case Some(product) =>
        if (!product.inStock) {
          BadRequest(createErrorResponse("Product is out of stock", "PRODUCT_UNAVAILABLE"))
        } else {
          // Check if item is already in cart
          val updatedItems = cart.items.find(_.productId == item.productId) match {
            case Some(existingItem) =>
              // Update quantity of existing item
              cart.items.map { i =>
                if (i.productId == item.productId) 
                  i.copy(quantity = i.quantity + item.quantity)
                else i
              }
            case None =>
              // Add new item to cart
              cart.items :+ item.copy(price = product.price)
          }
                
          val updatedCart = cart.copy(items = updatedItems)
          carts.update(cartId, updatedCart)
          Ok(Json.toJson(updatedCart))
        }
    }
  }
  
  /**
   * Create a standardized error response
   */
  private def createErrorResponse(message: String, errorCode: String = "ERROR"): JsObject = {
    Json.obj(
      "error" -> message,
      "code" -> errorCode
    )
  }
}