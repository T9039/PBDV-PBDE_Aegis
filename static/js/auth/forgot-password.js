document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('forgot-password-form');
    const resetBtn = document.getElementById('reset-btn');
    const alertBox = document.getElementById('reset-alert');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value.trim();
            
            // UI Feedback
            resetBtn.disabled = true;
            resetBtn.textContent = 'Sending...';
            resetBtn.classList.add('opacity-70', 'cursor-not-allowed');
            alertBox.classList.add('hidden');

            try {
                const response = await fetch('/forgot-password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });

                const data = await response.json();

                // Style the alert box for success
                alertBox.textContent = data.message;
                alertBox.className = 'mb-6 p-3 rounded-lg text-sm font-medium text-center transition-all text-emerald-400 bg-emerald-900/30 border border-emerald-800/50 block';
                
                // Clear the input so they don't submit twice
                document.getElementById('email').value = '';

            } catch (error) {
                alertBox.textContent = "A network error occurred. Please try again.";
                alertBox.className = 'mb-6 p-3 rounded-lg text-sm font-medium text-center transition-all text-red-400 bg-red-900/30 border border-red-800/50 block';
            } finally {
                // Restore button
                resetBtn.disabled = false;
                resetBtn.textContent = 'Send Reset Link';
                resetBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            }
        });
    }
});
