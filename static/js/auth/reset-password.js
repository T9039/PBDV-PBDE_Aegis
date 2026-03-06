document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('new-password-form');
    const submitBtn = document.getElementById('submit-btn');
    const alertBox = document.getElementById('reset-alert');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            alertBox.classList.add('hidden');

            // 1. Frontend Validation
            if (password !== confirmPassword) {
                alertBox.textContent = "Passwords do not match.";
                alertBox.className = 'mb-6 p-3 rounded-lg text-sm font-medium text-center transition-all text-red-400 bg-red-900/30 border border-red-800/50 block';
                return;
            }

            // 2. UI Feedback
            submitBtn.disabled = true;
            submitBtn.textContent = 'Updating...';
            submitBtn.classList.add('opacity-70', 'cursor-not-allowed');

            try {
                // We use the resetToken variable defined in the HTML <script> tag
                const response = await fetch(`/reset-password/${resetToken}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    alertBox.textContent = "Success! Redirecting to login...";
                    alertBox.className = 'mb-6 p-3 rounded-lg text-sm font-medium text-center transition-all text-emerald-400 bg-emerald-900/30 border border-emerald-800/50 block';
                    
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500);
                } else {
                    alertBox.textContent = data.message || "Failed to reset password.";
                    alertBox.className = 'mb-6 p-3 rounded-lg text-sm font-medium text-center transition-all text-red-400 bg-red-900/30 border border-red-800/50 block';
                }
            } catch (error) {
                alertBox.textContent = "Network error. Please try again.";
                alertBox.className = 'mb-6 p-3 rounded-lg text-sm font-medium text-center transition-all text-red-400 bg-red-900/30 border border-red-800/50 block';
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Update Password';
                submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            }
        });
    }
});
