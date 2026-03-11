document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('mentor-search');
    const mentorCards = document.querySelectorAll('.mentor-card');
    const noResultsMsg = document.getElementById('no-results');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');

    // Function to filter cards
    function filterMentors(query) {
        const lowerQuery = query.toLowerCase().trim();
        let visibleCount = 0;

        mentorCards.forEach(card => {
            // Grab the hidden search string we built in Jinja
            const searchData = card.getAttribute('data-search');
            
            if (searchData.includes(lowerQuery)) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Show/hide the "No Results" message
        if (visibleCount === 0) {
            noResultsMsg.classList.remove('hidden');
        } else {
            noResultsMsg.classList.add('hidden');
        }
    }

    // 1. Listen for typing in the search bar
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterMentors(e.target.value);
        });
    }

    // 2. Allow clicking the "Suggested" buttons to trigger a search
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.innerText;
            searchInput.value = query; // Fill the input box
            filterMentors(query);      // Run the filter
        });
    });
});
