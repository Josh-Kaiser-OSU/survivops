document.addEventListener('DOMContentLoaded', checkProductQty);

function checkProductQty() {
  let qty_available = parseInt(document.getElementById('qty_available').textContent, 10);
  // If a product is not available, disable all inputs and the submit button
  if (qty_available < 1) {
    disableForm();
  }
}

function disableForm() {
  let qty_to_order_field = document.getElementById('quantity-to-order');
  let cart_field = document.getElementById('cart-select');
  let submit_btn = document.getElementById('add-to-cart-btn');

  qty_to_order_field.toggleAttribute('disabled');
  cart_field.toggleAttribute('disabled');
  submit_btn.toggleAttribute('disabled');
}
