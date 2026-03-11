function openStudentEditModal() {
    const backdrop = document.getElementById('student-edit-backdrop');
    const box = document.getElementById('student-edit-box');
    
    // Remove FOUC inline styles
    backdrop.style.opacity = '';
    backdrop.style.pointerEvents = '';
    backdrop.style.position = '';
    backdrop.style.inset = '';
    
    backdrop.classList.remove('opacity-0', 'pointer-events-none');
    box.classList.remove('scale-95', 'opacity-0');
    box.classList.add('scale-100', 'opacity-100');
}

function closeStudentEditModal() {
    const backdrop = document.getElementById('student-edit-backdrop');
    const box = document.getElementById('student-edit-box');
    
    box.classList.remove('scale-100', 'opacity-100');
    box.classList.add('scale-95', 'opacity-0');
    
    setTimeout(() => {
      backdrop.classList.add('opacity-0', 'pointer-events-none');
    }, 200);
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('student-edit-form');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = "Saving...";
            submitBtn.disabled = true;

            const formData = new FormData(form);

            try {
                const response = await fetch('/student/edit-profile', {
                    method: 'POST',
                    body: formData 
                });

                const result = await response.json();

                if (result.success) {
                    showToast(result.message, "success");
                    closeStudentEditModal();
                    
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
});
