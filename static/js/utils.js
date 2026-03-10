/**
 * Displays a sliding toast notification on the screen.
 * @param {string} message - The text to display.
 * @param {string} type - 'success' (green) or 'error' (red).
 */
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) {
        console.error("Toast container missing from the HTML!");
        return;
    }

    const toast = document.createElement('div');
    
    // Base Tailwind classes for the pop-up
    toast.className = `flex items-center gap-3 px-5 py-3.5 rounded-xl shadow-2xl border transform transition-all duration-300 translate-x-full opacity-0 pointer-events-auto max-w-sm`;
    
    // Style differently based on Success or Error
    if (type === 'success') {
        toast.classList.add('bg-slate-900', 'border-emerald-500/30', 'text-slate-200');
        toast.innerHTML = `
            <div class="bg-emerald-500/20 p-1.5 rounded-lg">
                <svg class="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            </div>
            <span class="text-sm font-medium">${message}</span>
        `;
    } else {
        toast.classList.add('bg-slate-900', 'border-rose-500/30', 'text-slate-200');
        toast.innerHTML = `
            <div class="bg-rose-500/20 p-1.5 rounded-lg">
                <svg class="w-5 h-5 text-rose-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </div>
            <span class="text-sm font-medium">${message}</span>
        `;
    }

    container.appendChild(toast);

    // Trigger the slide-in animation
    requestAnimationFrame(() => {
        toast.classList.remove('translate-x-full', 'opacity-0');
    });

    // Remove the toast after 4 seconds
    setTimeout(() => {
        toast.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => toast.remove(), 300); // Wait for CSS transition to finish
    }, 4000);
}
