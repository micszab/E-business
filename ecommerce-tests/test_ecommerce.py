import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Helper Functions

def assert_element_text(driver, by_strategy, locator_value, expected_text, timeout=10):
    """
    Asserts that an element is visible and contains the expected text.
    Provides clear error messages if the condition is not met within the timeout.
    """
    try:
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_strategy, locator_value)))
        assert element.text.strip() == expected_text.strip(), \
            f"Assertion Failed: Expected text '{expected_text}', but found '{element.text}' for element located by {by_strategy}='{locator_value}'."
        print(f"PASS: Element with '{locator_value}' correctly displays text: '{expected_text}'.")
    except (TimeoutException, NoSuchElementException) as e:
        pytest.fail(f"Test Failed: Element with {by_strategy}='{locator_value}' not found or text mismatch. Details: {e}")

def assert_element_visible(driver, by_strategy, locator_value, timeout=10):
    """
    Asserts that an element is visible on the page within the given timeout.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_strategy, locator_value)))
        print(f"PASS: Element located by {by_strategy}='{locator_value}' is visible as expected.")
    except (TimeoutException, NoSuchElementException) as e:
        pytest.fail(f"Test Failed: Element located by {by_strategy}='{locator_value}' is NOT visible. Details: {e}")

def assert_element_not_visible(driver, by_strategy, locator_value, timeout=5):
    """
    Asserts that an element is NOT visible on the page within the given timeout.
    Useful for checking elements that should disappear (e.g., loading spinners, success messages).
    """
    try:
        WebDriverWait(driver, timeout).until_not(EC.visibility_of_element_located((by_strategy, locator_value)))
        print(f"PASS: Element located by {by_strategy}='{locator_value}' is not visible as expected.")
    except (TimeoutException, NoSuchElementException):
        assert not EC.visibility_of_element_located((by_strategy, locator_value))(driver), \
            f"Assertion Failed: Element located by {by_strategy}='{locator_value}' is still visible, but should not be."
        print(f"INFO: Element {by_strategy}='{locator_value}' might have briefly appeared, but condition for 'not visible' was met.")


def assert_button_enabled(driver, by_strategy, locator_value, timeout=10):
    """
    Asserts that a button element is enabled (clickable).
    """
    try:
        button = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by_strategy, locator_value)))
        assert button.is_enabled(), f"Assertion Failed: Button located by {by_strategy}='{locator_value}' should be enabled, but it's not."
        print(f"PASS: Button '{locator_value}' is correctly enabled.")
    except (TimeoutException, NoSuchElementException) as e:
        pytest.fail(f"Test Failed: Button '{locator_value}' not found or is not clickable. Details: {e}")

def assert_button_disabled(driver, by_strategy, locator_value, timeout=10):
    """
    Asserts that a button element is disabled (not clickable).
    """
    try:
        button = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by_strategy, locator_value)))
        assert not button.is_enabled(), f"Assertion Failed: Button located by {by_strategy}='{locator_value}' should be disabled, but it's active."
        print(f"PASS: Button '{locator_value}' is correctly disabled.")
    except (TimeoutException, NoSuchElementException) as e:
        pytest.fail(f"Test Failed: Button '{locator_value}' not found or is unexpectedly enabled. Details: {e}")

# --- 20 Test Cases with Multiple Assertions ---
# Each test case is designed to cover a specific user interaction or UI state.

# Test Case 1: Verify homepage loads correctly and main navigation elements are present.
def test_1_homepage_load_and_header(driver):
    print("\n--- Test 1: Verifying homepage load and header elements ---")
    driver.get("http://localhost:3000")
    assert_element_text(driver, By.TAG_NAME, "h1", "Sklep")
    assert_element_visible(driver, By.CLASS_NAME, "App-nav")
    assert_element_text(driver, By.XPATH, "//nav/a[text()='Produkty']", "Produkty")
    assert_element_text(driver, By.XPATH, "//nav/a[contains(text(),'Koszyk (0)')]", "Koszyk (0)")

# Test Case 2: Ensure product list is displayed and contains expected items.
def test_2_products_display(driver):
    print("\n--- Test 2: Checking product list display ---")
    assert_element_visible(driver, By.CLASS_NAME, "product-list")
    product_cards = driver.find_elements(By.CLASS_NAME, "product-card")
    assert len(product_cards) > 0, "Test Failed: No product cards were displayed."
    assert_element_text(driver, By.XPATH, "//div[@class='product-card'][1]/h3", "Zestaw klocków konstrukcyjnych")
    assert_element_text(driver, By.XPATH, "//div[@class='product-card'][1]/p[@class='price']", "129.99 PLN")

# Test Case 3: Add a single product to the cart and verify cart counter update.
def test_3_add_single_product_to_cart(driver):
    print("\n--- Test 3: Adding a single product to cart ---")
    driver.find_element(By.XPATH, "(//button[text()='Dodaj do koszyka'])[1]").click()
    assert_element_text(driver, By.XPATH, "//nav/a[contains(text(),'Koszyk (1)')]", "Koszyk (1)")

# Test Case 4: Navigate to the cart page and confirm the added product is displayed correctly.
def test_4_navigate_to_cart_and_verify_product(driver):
    print("\n--- Test 4: Navigating to cart and verifying product presence ---")
    driver.find_element(By.LINK_TEXT, "Koszyk (1)").click()
    assert_element_text(driver, By.TAG_NAME, "h2", "Twój Koszyk (1 przedmiotów)")
    assert_element_text(driver, By.XPATH, "//div[@class='cart-item-card']//h3", "Zestaw klocków konstrukcyjnych")
    assert_element_text(driver, By.XPATH, "//div[@class='cart-item-card']//span", "1")
    assert_element_text(driver, By.XPATH, "//div[@class='cart-item-card']//div[@class='item-total']", "Total: 129.99 PLN")

# Test Case 5: Increase the quantity of a product in the cart and check totals.
def test_5_increase_product_quantity_in_cart(driver):
    print("\n--- Test 5: Increasing product quantity in cart ---")
    driver.find_element(By.XPATH, "//div[@class='item-quantity-controls']/button[text()='+']").click()
    assert_element_text(driver, By.XPATH, "//div[@class='cart-item-card']//span", "2")
    assert_element_text(driver, By.XPATH, "//div[@class='cart-summary']//h3", "Całkowita wartość koszyka: 259.98 PLN")
    assert_element_text(driver, By.TAG_NAME, "h2", "Twój Koszyk (2 przedmiotów)")

# Test Case 6: Decrease the quantity of a product in the cart and check totals.
def test_6_decrease_product_quantity_in_cart(driver):
    print("\n--- Test 6: Decreasing product quantity in cart ---")
    driver.find_element(By.XPATH, "//div[@class='item-quantity-controls']/button[text()='-']").click()
    assert_element_text(driver, By.XPATH, "//div[@class='cart-item-card']//span", "1")
    assert_element_text(driver, By.XPATH, "//div[@class='cart-summary']//h3", "Całkowita wartość koszyka: 129.99 PLN")
    assert_element_text(driver, By.TAG_NAME, "h2", "Twój Koszyk (1 przedmiotów)")

# Test Case 7: Remove a product entirely from the cart.
def test_7_remove_product_from_cart(driver):
    print("\n--- Test 7: Removing product from cart ---")
    driver.find_element(By.CLASS_NAME, "remove-item-button").click()
    assert_element_text(driver, By.TAG_NAME, "h2", "Twój Koszyk (0 przedmiotów)")
    assert_element_visible(driver, By.CLASS_NAME, "empty-cart-message")
    assert_element_text(driver, By.CLASS_NAME, "empty-cart-message", "Twój koszyk jest pusty.")
    driver.find_element(By.LINK_TEXT, "Produkty").click()
    assert_element_text(driver, By.XPATH, "//nav/a[contains(text(),'Koszyk (0)')]", "Koszyk (0)")

# Test Case 8: Add multiple distinct products to the cart and verify total count.
def test_8_add_multiple_different_products(driver):
    print("\n--- Test 8: Adding multiple different products to cart ---")
    driver.find_element(By.XPATH, "(//button[text()='Dodaj do koszyka'])[1]").click()
    driver.find_element(By.XPATH, "(//button[text()='Dodaj do koszyka'])[2]").click()
    driver.find_element(By.XPATH, "(//button[text()='Dodaj do koszyka'])[3]").click()
    assert_element_text(driver, By.XPATH, "//nav/a[contains(text(),'Koszyk (3)')]", "Koszyk (3)")
    driver.find_element(By.LINK_TEXT, "Koszyk (3)").click()
    assert_element_text(driver, By.TAG_NAME, "h2", "Twój Koszyk (3 przedmiotów)")
    assert len(driver.find_elements(By.CLASS_NAME, "cart-item-card")) == 3, "Test Failed: Expected 3 distinct products in cart, but found different number."

# Test Case 9: Confirm the total amount calculation in the cart with multiple products.
def test_9_total_amount_with_multiple_products(driver):
    print("\n--- Test 9: Verifying total cart amount with multiple products ---")
    # This test assumes the previous test added products correctly.
    # Expected total is sum of: Klocki (129.99) + Miś (75.50) + Dron (249.00) = 454.49 PLN
    expected_total = (129.99 + 75.50 + 249.00)
    assert_element_text(driver, By.XPATH, "//div[@class='cart-summary']//h3", f"Całkowita wartość koszyka: {expected_total:.2f} PLN")

# Test Case 10: Attempt to proceed to checkout with an empty cart and verify alert.
def test_10_checkout_with_empty_cart(driver):
    print("\n--- Test 10: Attempting checkout with empty cart ---")
    driver.find_element(By.LINK_TEXT, "Koszyk (3)").click()
    # Empty the cart first by removing all items
    for _ in range(3):
        driver.find_element(By.CLASS_NAME, "remove-item-button").click()
        # Wait briefly for removal to process, or for empty cart message to appear
        WebDriverWait(driver, 5).until(lambda d: len(d.find_elements(By.CLASS_NAME, "cart-item-card")) == (2 - _) or EC.visibility_of_element_located((By.CLASS_NAME, "empty-cart-message")))

    assert_element_visible(driver, By.CLASS_NAME, "empty-cart-message")
    driver.find_element(By.CLASS_NAME, "checkout-button").click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Twój koszyk jest pusty!", "Test Failed: Alert message for empty cart was incorrect."
    alert.accept()
    assert driver.current_url.endswith("/cart"), "Test Failed: Should remain on cart page after empty cart alert."

# Test Case 11: Successfully submit the payment form with valid data.
def test_11_successful_payment_submission(driver):
    print("\n--- Test 11: Performing a successful payment submission ---")
    driver.get("http://localhost:3000")
    driver.find_element(By.XPATH, "(//button[text()='Dodaj do koszyka'])[1]").click()
    driver.find_element(By.LINK_TEXT, "Koszyk (1)").click()
    driver.find_element(By.CLASS_NAME, "checkout-button").click()

    assert driver.current_url.endswith("/payments"), "Test Failed: Did not navigate to /payments page."
    assert_element_text(driver, By.TAG_NAME, "h2", "Płatność")

    # Fill out the payment form fields
    driver.find_element(By.ID, "cardNumber").send_keys("1234567812345678")
    driver.find_element(By.ID, "expiryDate").send_keys("12/25")
    driver.find_element(By.ID, "cvv").send_keys("123")
    driver.find_element(By.ID, "customerName").send_keys("Jan Kowalski")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert_element_visible(driver, By.CLASS_NAME, "payment-message.success")
    assert_element_text(driver, By.CLASS_NAME, "payment-message.success", "Płatność pomyślna!")

# Test Case 12: Validate payment form requires card number (using HTML5 validation).
def test_12_payment_form_validation_card_number(driver):
    print("\n--- Test 12: Payment form validation - missing card number ---")
    driver.get("http://localhost:3000/payments")
    assert_element_text(driver, By.TAG_NAME, "h2", "Płatność")

    # Clear card number and fill others
    driver.find_element(By.ID, "cardNumber").clear()
    driver.find_element(By.ID, "expiryDate").send_keys("12/25")
    driver.find_element(By.ID, "cvv").send_keys("123")
    driver.find_element(By.ID, "customerName").send_keys("Test Walidacji")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert_element_not_visible(driver, By.CLASS_NAME, "payment-message.success")
    assert_element_visible(driver, By.ID, "cardNumber")
    # Check HTML5 form validation for 'required' attribute
    assert driver.execute_script("return document.getElementById('cardNumber').checkValidity()") == False, \
        "Test Failed: Card number field should be invalid due to missing input."

# Test Case 13: Validate payment form requires expiry date.
def test_13_payment_form_validation_expiry_date(driver):
    print("\n--- Test 13: Payment form validation - missing expiry date ---")
    driver.get("http://localhost:3000/payments")
    driver.find_element(By.ID, "cardNumber").send_keys("1234567812345678")
    driver.find_element(By.ID, "expiryDate").clear()
    driver.find_element(By.ID, "cvv").send_keys("123")
    driver.find_element(By.ID, "customerName").send_keys("Test Walidacji")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert_element_not_visible(driver, By.CLASS_NAME, "payment-message.success")
    assert driver.execute_script("return document.getElementById('expiryDate').checkValidity()") == False, \
        "Test Failed: Expiry date field should be invalid due to missing input."

# Test Case 14: Validate payment form requires CVV.
def test_14_payment_form_validation_cvv(driver):
    print("\n--- Test 14: Payment form validation - missing CVV ---")
    driver.get("http://localhost:3000/payments")
    driver.find_element(By.ID, "cardNumber").send_keys("1234567812345678")
    driver.find_element(By.ID, "expiryDate").send_keys("12/25")
    driver.find_element(By.ID, "cvv").clear()
    driver.find_element(By.ID, "customerName").send_keys("Test Walidacji")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert_element_not_visible(driver, By.CLASS_NAME, "payment-message.success")
    assert driver.execute_script("return document.getElementById('cvv').checkValidity()") == False, \
        "Test Failed: CVV field should be invalid due to missing input."

# Test Case 15: Validate payment form requires customer name.
def test_15_payment_form_validation_customer_name(driver):
    print("\n--- Test 15: Payment form validation - missing customer name ---")
    driver.get("http://localhost:3000/payments")
    driver.find_element(By.ID, "cardNumber").send_keys("1234567812345678")
    driver.find_element(By.ID, "expiryDate").send_keys("12/25")
    driver.find_element(By.ID, "cvv").send_keys("123")
    driver.find_element(By.ID, "customerName").clear()
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert_element_not_visible(driver, By.CLASS_NAME, "payment-message.success")
    assert driver.execute_script("return document.getElementById('customerName').checkValidity()") == False, \
        "Test Failed: Customer Name field should be invalid due to missing input."

# Test Case 16: Verify navigation between Products and Cart pages works as expected.
def test_16_navigation_between_products_and_cart(driver):
    print("\n--- Test 16: Checking navigation between Products and Cart ---")
    driver.get("http://localhost:3000")
    assert_element_visible(driver, By.CLASS_NAME, "product-list")
    driver.find_element(By.LINK_TEXT, "Koszyk (0)").click()
    assert_element_visible(driver, By.CLASS_NAME, "cart-container")
    assert_element_text(driver, By.TAG_NAME, "h2", "Twój Koszyk (0 przedmiotów)")
    driver.find_element(By.LINK_TEXT, "Produkty").click()
    assert_element_visible(driver, By.CLASS_NAME, "products-container")
    assert_element_text(driver, By.TAG_NAME, "h2", "Dostępne Produkty")

# Test Case 17: Verify the browser window title remains consistent across different routes.
def test_17_page_title_after_navigation(driver):
    print("\n--- Test 17: Verifying browser page title consistency ---")
    driver.get("http://localhost:3000")
    assert driver.title == "React App", "Test Failed: Homepage title mismatch."
    driver.find_element(By.LINK_TEXT, "Koszyk (0)").click()
    assert driver.title == "React App", "Test Failed: Cart page title mismatch."
    driver.find_element(By.CLASS_NAME, "checkout-button").click()
    assert driver.title == "React App", "Test Failed: Payments page title mismatch."

# Test Case 18: Add a product, refresh the page, and verify the cart state resets (as it's not persistent).
def test_18_add_product_and_refresh(driver):
    print("\n--- Test 18: Checking cart state after page refresh ---")
    driver.get("http://localhost:3000")
    driver.find_element(By.XPATH, "(//button[text()='Dodaj do koszyka'])[1]").click()
    assert_element_text(driver, By.XPATH, "//nav/a[contains(text(),'Koszyk (1)')]", "Koszyk (1)")
    driver.refresh()
    assert_element_text(driver, By.XPATH, "//nav/a[contains(text(),'Koszyk (0)')]", "Koszyk (0)")
    assert len(driver.find_elements(By.CLASS_NAME, "product-card")) > 0, "Products should still be visible after refresh."

# Test Case 19: Verify "Add to cart" button is enabled for products.
def test_19_add_to_cart_button_enabled(driver):
    print("\n--- Test 19: Verifying 'Add to cart' button is enabled ---")
    driver.get("http://localhost:3000")
    assert_button_enabled(driver, By.XPATH, "(//button[text()='Dodaj do koszyka'])[1]")
    assert_button_enabled(driver, By.XPATH, "(//button[text()='Dodaj do koszyka'])[2]")

# Test Case 20: Verify "Proceed to checkout" button behavior in an empty cart.
def test_20_checkout_button_in_empty_cart(driver):
    print("\n--- Test 20: Checking checkout button behavior with empty cart ---")
    driver.get("http://localhost:3000/cart")
    assert_element_visible(driver, By.CLASS_NAME, "empty-cart-message")
    checkout_button = driver.find_element(By.CLASS_NAME, "checkout-button")
    checkout_button.click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Twój koszyk jest pusty!", "Test Failed: Alert message for empty cart was incorrect."
    alert.accept()
    assert_button_enabled(driver, By.CLASS_NAME, "checkout-button") # Button remains enabled, but alert prevents navigation
