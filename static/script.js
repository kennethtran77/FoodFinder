function handleFlash(message) {
    if (message)
        alert(message);
}

// Prevent enter submitting
document.querySelector("form").onkeypress = function(e) {
  var key = e.charCode || e.keyCode || 0;

  if (key == 13) {
    e.preventDefault();
  }
}
