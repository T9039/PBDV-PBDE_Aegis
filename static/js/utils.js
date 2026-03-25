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



// ==========================================
// GLOBAL CUSTOM CONFIRM MODAL
// ==========================================
function customConfirm(message, title, onConfirmCallback) {
    // 1. Check if the modal already exists in the DOM
    let modal = document.getElementById('global-confirm-modal');

    // 2. If it doesn't exist yet, build the HTML dynamically!
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'global-confirm-modal';
        modal.className = 'modal-overlay';
        modal.style.zIndex = '10000'; // Keep it above all other modals

        modal.innerHTML = `
            <div class="modal-box max-w-sm text-center">
                <div class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style="background: #fee2e2">
                    <svg class="w-8 h-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                </div>
                <h2 class="text-lg font-bold mb-2 text-gray-800" id="global-confirm-title"></h2>
                <p class="text-sm text-gray-500 mb-6" id="global-confirm-message"></p>
                <div class="flex gap-3">
                    <button id="global-confirm-cancel" class="btn-sm bg-gray-100 text-gray-700 hover:bg-gray-200 flex-1 py-2 rounded-lg font-semibold transition-colors">Cancel</button>
                    <button id="global-confirm-action" class="btn-sm bg-red-600 text-white hover:bg-red-700 flex-1 py-2 rounded-lg font-semibold transition-colors">Confirm</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Wire up the static Cancel button
        document.getElementById('global-confirm-cancel').addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

    // 3. Inject the custom text for this specific action
    document.getElementById('global-confirm-title').textContent = title || "Are you sure?";
    document.getElementById('global-confirm-message').textContent = message;

    // 4. Wire up the Confirm button
    // We clone the button first to wipe out any old event listeners from previous confirms!
    const actionBtn = document.getElementById('global-confirm-action');
    const newActionBtn = actionBtn.cloneNode(true);
    actionBtn.parentNode.replaceChild(newActionBtn, actionBtn);

    newActionBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        if (onConfirmCallback) onConfirmCallback();
    });

    // 5. Show the modal
    modal.classList.add('active');
}


