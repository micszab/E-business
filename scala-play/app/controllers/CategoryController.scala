package controllers

import javax.inject._
import play.api.mvc._
import play.api.libs.json._
import scala.collection.mutable.ListBuffer

/**
 * Model class representing a product category
 *
 * @param id Unique identifier for the category
 * @param name Category name
 * @param description Brief description of the category
 */
case class Category(
  id: Int,
  name: String,
  description: String
)

object Category {
  // JSON formatter for Category class
  implicit val categoryFormat: OFormat[Category] = Json.format[Category]
}

/**
 * Controller handling CRUD operations for categories.
 */
@Singleton
class CategoryController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  
  // In-memory category database (pre-populated with the same categories used in ProductController)
  private val categories = ListBuffer(
    Category(1, "Electronics", "Electronic devices and gadgets"),
    Category(2, "Clothing", "Apparel and fashion items"),
    Category(3, "Books", "Books and publications")
  )
  
  /**
   * @return JSON array of all categories
   */
  def getAll: Action[AnyContent] = Action {
    Ok(Json.toJson(categories))
  }
  
  /**
   * @param id The category ID to look up
   * @return JSON of the category or 404 if not found
   */
  def getById(id: Int): Action[AnyContent] = Action {
    findCategoryById(id) match {
      case Some(category) => Ok(Json.toJson(category))
      case None => NotFound(createErrorResponse("Category not found", "NOT_FOUND"))
    }
  }
  
  /**
   * Creates a new category
   * @return Created status with the new category as JSON
   */
  def add: Action[JsValue] = Action(parse.json) { request =>
    request.body.validate[Category].fold(
      errors => {
        BadRequest(createErrorResponse("Invalid category data: " + JsError.toJson(errors), "VALIDATION_ERROR"))
      },
      category => {
        val newId = if (categories.isEmpty) 1 else categories.map(_.id).max + 1
        val newCategory = category.copy(id = newId)
        categories += newCategory
        Created(Json.toJson(newCategory))
          .withHeaders("Location" -> s"/categories/$newId")
      }
    )
  }
  
  /**
   * Updates an existing category
   * @param id The ID of the category to update
   * @return OK with the updated category or 404 if not found
   */
  def update(id: Int): Action[JsValue] = Action(parse.json) { request =>
    request.body.validate[Category].fold(
      errors => {
        BadRequest(createErrorResponse("Invalid category data: " + JsError.toJson(errors), "VALIDATION_ERROR"))
      },
      updatedCategory => {
        categories.indexWhere(_.id == id) match {
          case -1 => NotFound(createErrorResponse("Category not found", "NOT_FOUND"))
          case index =>
            categories.update(index, updatedCategory.copy(id = id))
            Ok(Json.toJson(updatedCategory.copy(id = id)))
        }
      }
    )
  }
  
  /**
   * Delete a category by its ID
   * 
   * @param id The ID of the category to delete
   * @return NoContent if successful or 404 if not found
   */
  def delete(id: Int): Action[AnyContent] = Action {
    categories.indexWhere(_.id == id) match {
      case -1 => NotFound(createErrorResponse("Category not found", "NOT_FOUND"))
      case index =>
        categories.remove(index)
        NoContent
    }
  }
  
  // Helper methods
  private def findCategoryById(id: Int): Option[Category] = {
    categories.find(_.id == id)
  }
  
  private def createErrorResponse(message: String, errorCode: String = "ERROR"): JsObject = {
    Json.obj(
      "error" -> message,
      "code" -> errorCode
    )
  }
}