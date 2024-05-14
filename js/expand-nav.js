document.addEventListener("DOMContentLoaded", function () {
  var toggles = document.querySelectorAll('.md-nav__toggle');
  for (var i = 0; i < toggles.length; i++) {
    toggles[i].checked = true; // This sets the toggle to the "open" position
  }
});

