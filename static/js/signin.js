/*
Some of the code in this file is courtesy of CS 290 course materials, especially
Timothy Yoon's HW Assignment 6. Such code includes:
a. Creating and sending HTTP requests
(https://eecs.oregonstate.edu/ecampus-video/CS290/core-content/ajax-forms/js-http.html)
b. Creating and using promises
*/

const req_url = "./signin";

// Add click event listeners to all buttons on the page once the HTML is
// loaded and parsed
document.addEventListener('DOMContentLoaded', signInListener);
// document.addEventListener('DOMContentLoaded', signUpListener);  // todo

function signInListener() {
  let sign_in_button = document.getElementById('sign-in-button');
  sign_in_button.addEventListener('click', requestUserSignIn);
}

function requestUserSignIn {
  // Send a GET request to the server
  let req = new XMLHttpRequest();
  req.open('GET', req_url, false);
  req.setRequestHeader('Content-Type', 'application/json');
  req.send(null);
  // todo
}
