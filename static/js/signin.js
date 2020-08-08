let sign_up_btn = document.getElementById('sign-up-button');

// Disable the sign-up button when the HTML is loaded and parsed
document.addEventListener('DOMContentLoaded', toggleDisableSignUp);

// Toggle the disabling of the sign-up button
function toggleDisableSignUp() {
  sign_up_btn.toggleAttribute('disabled');
}

let firstPwdField = document.getElementById('sign-up-password-field');
let secondPwdField = document.getElementById('sign-up-confirm-password-field');

// Whenever the sign-up password fields are changed, check whether
// they hold equal values
firstPwdField.addEventListener('input', pwdListener);
secondPwdField.addEventListener('input', pwdListener);

function pwdListener() {
  // If the first and second passwords are equal, enable the sign-up button
  if (firstPwdField.value === secondPwdField.value) {
    toggleDisableSignUp();
  }
  // If the button is enabled and the passwords are not equal, disable the button
  else if (!(sign_up_btn.hasAttribute('disabled')) && (firstPwdField.value !== secondPwdField.value)) {
    toggleDisableSignUp();
  }
}
