document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const authAlert = document.getElementById('auth-alert');
    const submitBtn = document.getElementById('submit-btn');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            // Prevent standard HTML form submission
            e.preventDefault();
            
            // Reset the alert box
            authAlert.classList.add('hidden');
            authAlert.textContent = '';
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // UI Feedback: Show a loading state
            const originalBtnText = submitBtn.textContent;
            submitBtn.textContent = 'Verifying...';
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-70', 'cursor-not-allowed');

            try {
                // Send the request to your Flask backend prototype route
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    // Status 200: Credentials matched, redirect to OTP verification
                    window.location.href = data.redirect;
                } else {
                    // Status 400/401: Something went wrong, show the error
                    authAlert.textContent = data.message || 'Invalid campus credentials. Please try again.';
                    authAlert.classList.remove('hidden');
                }
            } catch (error) {
                // Handle network errors (e.g., server is down)
                authAlert.textContent = 'Network error. Please ensure the server is running.';
                authAlert.classList.remove('hidden');
            } finally {
                // Restore the button to its normal state
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            }
        });
    }
});
