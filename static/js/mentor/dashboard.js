document.addEventListener('DOMContentLoaded', () => {
  const backdrop = document.getElementById('modal-backdrop');
  const box = document.getElementById('modal-box');

  // Safety check: If the modal isn't on the page (profile is complete), do nothing!
  if (!backdrop || !box) return;

  // Make functions globally available so the HTML onclick="" attributes can find them
  window.openProfileModal = function() {
    backdrop.classList.remove('opacity-0', 'pointer-events-none');
    backdrop.classList.add('opacity-100', 'pointer-events-auto');

    backdrop.style.opacity = '';
    backdrop.style.pointerEvents = '';
    
    box.classList.remove('scale-75', 'opacity-0');
    box.classList.add('scale-100', 'opacity-100');
  };

  window.closeProfileModal = function() {
    backdrop.classList.remove('opacity-100', 'pointer-events-auto');
    backdrop.classList.add('opacity-0', 'pointer-events-none');
    
    box.classList.remove('scale-100', 'opacity-100');
    box.classList.add('scale-75', 'opacity-0');
  };

  // Automatically trigger the animation 1.5 seconds after the page loads
  setTimeout(() => {
    window.openProfileModal();
  }, 1000); 


    // --- NEW: Handle the form submission via fetch ---
  const profileForm = document.querySelector('#modal-box form');
  
  if (profileForm) {
    profileForm.addEventListener('submit', async (e) => {
      e.preventDefault(); 
      
      const submitBtn = profileForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerText;
      submitBtn.innerText = "Uploading Application...";
      submitBtn.disabled = true;

      // 1. Grab all the data, INCLUDING the files, straight from the form
      const formData = new FormData(profileForm);

      try {
        const response = await fetch('/mentor/complete-profile', {
          method: 'POST',
          // 2. CRITICAL: Do NOT set the 'Content-Type' header here. 
          // The browser will automatically set it to 'multipart/form-data' 
          // and inject the required boundary string for the files.
          body: formData
        });

        const result = await response.json();

        if (result.success) {
          window.location.reload();
        } else {
          alert(result.error || result.message || "Something went wrong saving your profile.");
          submitBtn.innerText = originalText;
          submitBtn.disabled = false;
        }
      } catch (error) {
        console.error("Error submitting profile:", error);
        alert("A network error occurred. Please try again.");
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
      }
    });
  }
});
