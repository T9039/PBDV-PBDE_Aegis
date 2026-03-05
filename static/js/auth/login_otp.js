document.addEventListener('DOMContentLoaded', () => {
    const otpForm = document.getElementById('otp-form');
    const otpAlert = document.getElementById('otp-alert');
    const verifyBtn = document.getElementById('verify-btn');
    const resendBtn = document.getElementById('resend-btn');
    const otpInput = document.getElementById('otp-code');

    if (otpForm) {
        otpForm.addEventListener('submit', async (e) => {
            // Prevent standard form submission
            e.preventDefault();
            
            // Clear any previous errors
            otpAlert.classList.add('hidden');
            otpAlert.textContent = '';
            
            // Grab the OTP value
            const otpValue = otpInput.value.trim();

            // Quick frontend check so we don't bother the server with empty submissions
            if (otpValue.length !== 6) {
                otpAlert.textContent = 'Please enter the full 6-digit code.';
                otpAlert.classList.remove('hidden');
                return;
            }

            // UI Feedback: Show a loading state so the user knows it's working
            const originalBtnText = verifyBtn.textContent;
            verifyBtn.textContent = 'Verifying...';
            verifyBtn.disabled = true;
            verifyBtn.classList.add('opacity-70', 'cursor-not-allowed');

            try {
                // Send the OTP back to your Flask backend (adjust the URL if your route is named differently)
                const response = await fetch('/login/otp', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ otp: otpValue })
                });

                const data = await response.json();

                if (response.ok && data.redirect_url) {
                    // Success! The server validated the OTP and told us where to go next.
                    window.location.href = data.redirect_url;
                } else {
                    // Failure! (e.g., Wrong OTP, expired OTP)
                    console.log(data.expiry)
                    otpAlert.textContent = data.error || 'Invalid verification code. Please try again.';
                    otpAlert.classList.remove('hidden');
                    
                    // Clear the input so they can easily type a new one
                    otpInput.value = '';
                    otpInput.focus();
                }
            } catch (error) {
                // Handle network crashes or server drops
                otpAlert.textContent = 'Network error. Please check your connection to the server.';
                otpAlert.classList.remove('hidden');
            } finally {
                // Restore the button to its normal, clickable state
                verifyBtn.textContent = originalBtnText;
                verifyBtn.disabled = false;
                verifyBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            }
        });
    }


    if (resendBtn) {
        resendBtn.addEventListener('click', async (e) => {
            e.preventDefault(); // Prevent any default anchor behavior

            // 1. UI Feedback: Disable button immediately
            resendBtn.disabled = true;
            const originalText = resendBtn.textContent;
            resendBtn.textContent = 'Sending...';
            resendBtn.classList.add('opacity-50', 'cursor-not-allowed');

            try {
                const response = await fetch('/login/otp/resend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    // 2. Show success message (using the same alert box from before)
                    const otpAlert = document.getElementById('otp-alert');
                    otpAlert.textContent = data.message;
                    otpAlert.classList.remove('hidden', 'text-red-400', 'bg-red-900/30', 'border-red-800/50');
                    
                    // Switch alert to "success" colors (Emerald)
                    otpAlert.classList.add('text-emerald-400', 'bg-emerald-900/30', 'border-emerald-800/50');

                    // 3. Start a 60-second cooldown timer
                    startResendCooldown(60);
                } else {
                    alert(data.message || "Failed to resend OTP.");
                    resendBtn.disabled = false;
                    resendBtn.textContent = originalText;
                    resendBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                }
            } catch (error) {
                console.error("Resend error:", error);
                resendBtn.disabled = false;
                resendBtn.textContent = originalText;
            }
        });
    }

    // Helper function to handle the cooldown logic
    function startResendCooldown(seconds) {
        const resendBtn = document.getElementById('resend-btn');
        let timeLeft = seconds;

        const timer = setInterval(() => {
            if (timeLeft <= 0) {
                clearInterval(timer);
                resendBtn.disabled = false;
                resendBtn.textContent = 'Resend';
                resendBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                resendBtn.textContent = `Resend in ${timeLeft}s`;
                timeLeft--;
            }
        }, 1000);
    }
});
