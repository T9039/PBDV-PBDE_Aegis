document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('new-password-form');
    const submitBtn = document.getElementById('submit-btn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            if (password !== confirmPassword) {
                return showToast("Passwords do not match.", "error");
            }

            submitBtn.disabled = true;
            submitBtn.textContent = 'Updating...';

            try {
                const response = await fetch(`/reset-password/${resetToken}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    showToast("Success! Redirecting to login...", "success");
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500);
                } else {
                    showToast(data.message || "Failed to reset password.", "error");
                }
            } catch (error) {
                showToast("Network error. Please try again.", "error");
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Update Password';
            }
        });
    }
});
