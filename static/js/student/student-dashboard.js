// 1. MODAL TOGGLE FUNCTIONS
function openStudentProfileModal() {
    const backdrop = document.getElementById('student-modal-backdrop');
    const box = document.getElementById('student-modal-box');
    
    if (!backdrop || !box) return; // Safety check

    // Remove FOUC inline styles
    backdrop.style.opacity = '';
    backdrop.style.pointerEvents = '';
    backdrop.style.position = '';
    backdrop.style.inset = '';
    
    backdrop.classList.remove('opacity-0', 'pointer-events-none');
    box.classList.remove('scale-95', 'opacity-0');
    box.classList.add('scale-100', 'opacity-100');
}

function closeStudentProfileModal(showWarning = false) {
    const backdrop = document.getElementById('student-modal-backdrop');
    const box = document.getElementById('student-modal-box');
    
    if (!backdrop || !box) return; // Safety check
    
    // Trigger the CSS shrink/fade animations
    box.classList.remove('scale-100', 'opacity-100');
    box.classList.add('scale-95', 'opacity-0');
    
    // Wait for the transition to finish before hiding the backdrop
    setTimeout(() => {
      backdrop.classList.add('opacity-0', 'pointer-events-none');
    }, 200);

    // If they clicked the 'X', show the warning toast
    if (showWarning) {
        setTimeout(() => {
            showToast("Without completing your details, the matchmaking system won't work for you.", "error");
        }, 300);
    }
}


// 2. DOM INITIALIZATION (Search & Form)
document.addEventListener('DOMContentLoaded', () => {
    
    // --- A. MODAL LOGIC ---
    const form = document.getElementById('student-profile-form');
    const backdrop = document.getElementById('student-modal-backdrop');

    // If the modal was rendered by Jinja, trigger it to open
    if (backdrop) {
        setTimeout(openStudentProfileModal, 300);
    }

    // If the form exists, attach the submit listener
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = "Saving...";
            submitBtn.disabled = true;

            const formData = new FormData(form);

            try {
                const response = await fetch('/student/complete-profile', {
                    method: 'POST',
                    body: formData 
                });

                const result = await response.json();

                if (result.success) {
                    showToast(result.message, "success");
                    
                    // Wait for the user to read the toast, then reload
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    showToast(result.error || "Something went wrong.", "error");
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                }
            } catch (error) {
                console.error("Error:", error);
                showToast("A network error occurred. Please try again.", "error");
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        });
    }

    // --- B. LIVE SEARCH LOGIC ---
    const searchInput = document.getElementById('mentor-search');
    const mentorCards = document.querySelectorAll('.mentor-card');
    const noResultsMsg = document.getElementById('no-results');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');

    function filterMentors(query) {
        const lowerQuery = query.toLowerCase().trim();
        let visibleCount = 0;

        mentorCards.forEach(card => {
            const searchData = card.getAttribute('data-search');
            if (searchData && searchData.includes(lowerQuery)) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        if (noResultsMsg) {
            if (visibleCount === 0) {
                noResultsMsg.classList.remove('hidden');
            } else {
                noResultsMsg.classList.add('hidden');
            }
        }
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterMentors(e.target.value);
        });
    }

    if (suggestionBtns) {
        suggestionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const query = btn.innerText;
                searchInput.value = query; 
                filterMentors(query);      
            });
        });
    }
});
