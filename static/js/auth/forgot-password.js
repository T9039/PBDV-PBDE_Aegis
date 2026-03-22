document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('forgot-password-form');
    const resetBtn = document.getElementById('reset-btn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            
            resetBtn.disabled = true;
            resetBtn.textContent = 'Sending...';

            try {
                const response = await fetch('/forgot-password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });

                const data = await response.json();
                
                showToast(data.message, data.success ? 'success' : 'error');
                if (data.success) document.getElementById('email').value = '';

            } catch (error) {
                showToast("A network error occurred. Please try again.", "error");
            } finally {
                resetBtn.disabled = false;
                resetBtn.textContent = 'Send Reset Link';
            }
        });
    }
});
