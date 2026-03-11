// --- Modal Toggle Functions ---
function openEditModal() {
    const backdrop = document.getElementById('edit-modal-backdrop');
    const box = document.getElementById('edit-modal-box');

    backdrop.style.opacity = '';
    backdrop.style.pointerEvents = '';
    
    backdrop.classList.remove('opacity-0', 'pointer-events-none');
    box.classList.remove('scale-95', 'opacity-0');
    box.classList.add('scale-100', 'opacity-100');
}

function closeEditModal() {
    const backdrop = document.getElementById('edit-modal-backdrop');
    const box = document.getElementById('edit-modal-box');
    
    box.classList.remove('scale-100', 'opacity-100');
    box.classList.add('scale-95', 'opacity-0');
    
    setTimeout(() => {
      backdrop.classList.add('opacity-0', 'pointer-events-none');
    }, 200);
}

// --- Form Submission Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const editForm = document.getElementById('edit-profile-form');
    
    if (editForm) {
        editForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Stop the default HTML page refresh
            
            const submitBtn = editForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = "Saving...";
            submitBtn.disabled = true;

            const formData = new FormData(editForm);

            try {
                const response = await fetch('/mentor/edit-profile', {
                    method: 'POST',
                    body: formData 
                });

                const result = await response.json();

                if (result.success) {
                    // 1. THIS IS WHERE IT IS CALLED! 
                    // It pulls 'showToast' from your global utils.js file
                    showToast(result.message || "Profile updated successfully!", "success");
                    
                    // 2. Hide the modal immediately so they can see the toast
                    closeEditModal(); 
                    
                    // 3. Wait 1.5 seconds so they can read it, then reload the page
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);

                } else {
                    // Trigger the red error toast
                    showToast(result.error || result.message || "Something went wrong.", "error");
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                }
            } catch (error) {
                console.error("Error updating profile:", error);
                // Trigger the red error toast for network failures
                showToast("A network error occurred. Please try again.", "error");
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        });
    }
});
