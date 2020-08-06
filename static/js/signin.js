/*
Some of the code in this file is courtesy of CS 290 course materials, especially
Timothy Yoon's HW Assignment 6. Such code includes:
a. Creating and sending HTTP requests
(https://eecs.oregonstate.edu/ecampus-video/CS290/core-content/ajax-forms/js-http.html)
*/

const req_url = "./signin";

// Add click event listeners to all buttons on the page once the HTML is
// loaded and parsed
document.addEventListener('DOMContentLoaded', addBtnListeners);

function addBtnListeners() {
  // Get the sign in and sign up buttons
  let sign_in_button = document.getElementById('sign-in-button');
  let sign_up_button = document.getElementById('sign-up-button');

  // Add click event listener to the sign in button
  sign_in_button.addEventListener('click', function() {
    // Send a GET request to the server
    let req = new XMLHttpRequest();
    req.open('GET', req_url, false);
    //
    // Todo
    //
  });
}
