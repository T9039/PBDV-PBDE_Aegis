document.addEventListener('DOMContentLoaded', () => {
  const backdrop = document.getElementById('modal-backdrop');
  const box = document.getElementById('modal-box');

  // Safety check: If the modal isn't on the page (profile is complete), do nothing!
  if (!backdrop || !box) return;

  // Make functions globally available so the HTML onclick="" attributes can find them
  window.openProfileModal = function() {
    backdrop.classList.remove('opacity-0', 'pointer-events-none');
    backdrop.classList.add('opacity-100', 'pointer-events-auto');
    
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
      e.preventDefault(); // Stop the browser from refreshing the page
      
      // Grab the submit button so we can show a loading state
      const submitBtn = profileForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerText;
      submitBtn.innerText = "Saving...";
      submitBtn.disabled = true;

      // Convert the form fields into a JSON object
      const formData = new FormData(profileForm);
      const data = Object.fromEntries(formData.entries());

      try {
        const response = await fetch('/mentor/complete-profile', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
          // Success! Reload the page to permanently hide the modal and update the UI
          window.location.reload();
        } else {
          alert(result.error || "Something went wrong saving your profile.");
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
