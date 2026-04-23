document.addEventListener('invalid', (function() {
  return function(e) {
    // This stops the browser's default popup bubble
    e.preventDefault();
  };
})(), true);