document.addEventListener('invalid', (function() {
  return function(e) {
    // Only prevent popup for search bar
    if (e.target.closest('.search-input-container')) {
      e.preventDefault();
    }
  };
})(), true);