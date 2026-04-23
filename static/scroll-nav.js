// Scroll-to-Letter Navigation System
// Handles click-to-scroll functionality and dynamic letter highlighting

document.addEventListener('DOMContentLoaded', function() {
    const letterLinks = document.querySelectorAll('.az-list-item');
    const galleryContainer = document.querySelector('.grid-container');
    const galleryItems = document.querySelectorAll('.grid-item');

    // Track the currently active letter (for avoiding redundant updates)
    let currentActiveLetter = null;

    /**
     * Set the active letter in the sidebar
     * @param {string} letter - The letter to mark as active
     */
    function setActiveLetter(letter) {
        if (currentActiveLetter === letter) return;
        
        // Remove active class from all letter links
        letterLinks.forEach(link => link.classList.remove('active'));
        
        // Add active class to the matching letter link
        const activeLink = document.querySelector(`.az-list-item[data-letter="${letter}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
            currentActiveLetter = letter;
        }
    }

    /**
     * Scroll to the first item matching a specific letter
     * Only scrolls the gallery container, not parent elements (keeps navbar visible)
     * @param {string} letter - The letter to scroll to
     */
    function scrollToLetter(letter) {
        const firstItem = document.querySelector(`.grid-item[data-letter="${letter}"]`);
        if (firstItem && galleryContainer) {
            // Calculate the scroll position relative to the container
            // We need to account for the item's position within the scrollable container
            const containerScrollTop = galleryContainer.scrollTop;
            const itemPosition = firstItem.getBoundingClientRect();
            const containerPosition = galleryContainer.getBoundingClientRect();
            
            // Calculate where to scroll to
            const scrollTo = containerScrollTop + (itemPosition.top - containerPosition.top);
            
            // Smooth scroll only the gallery container
            galleryContainer.scrollTo({
                top: scrollTo,
                behavior: 'smooth'
            });
            
            setActiveLetter(letter);
        }
    }

    /**
     * Update active letter based on current scroll position
     * Finds the topmost visible item in the gallery container
     */
    function updateActiveLetter() {
        if (!galleryContainer) return;

        let topVisibleLetter = null;
        let topVisiblePosition = Infinity;

        // Check all gallery items to find which is topmost and visible
        galleryItems.forEach(item => {
            const rect = item.getBoundingClientRect();
            const containerRect = galleryContainer.getBoundingClientRect();
            
            // Calculate item position relative to container
            const itemTop = rect.top - containerRect.top;
            
            // Check if item is within or near the visible container
            if (itemTop < containerRect.height && itemTop + rect.height > 0) {
                const letter = item.dataset.letter;
                
                // Track the item closest to the top
                if (itemTop < topVisiblePosition) {
                    topVisiblePosition = itemTop;
                    topVisibleLetter = letter;
                }
            }
        });

        // Update active letter if we found a visible one
        if (topVisibleLetter) {
            setActiveLetter(topVisibleLetter);
        }
    }

    /**
     * Setup scroll event listener with throttling for performance
     * This updates the active letter as the user scrolls (both up and down)
     */
    function setupScrollListener() {
        if (!galleryContainer) return;

        let scrollTimeout;
        
        galleryContainer.addEventListener('scroll', function() {
            // Throttle the scroll event to run at most every 50ms for performance
            if (scrollTimeout) {
                clearTimeout(scrollTimeout);
            }
            
            scrollTimeout = setTimeout(function() {
                updateActiveLetter();
            }, 50);
        });

        // Update immediately on load
        updateActiveLetter();
    }

    /**
     * Setup click event listeners on letter links
     */
    function setupLetterClickHandlers() {
        letterLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const letter = this.dataset.letter;
                scrollToLetter(letter);
            });
        });
    }

    // Initialize all functionality
    setupLetterClickHandlers();
    setupScrollListener();
});
