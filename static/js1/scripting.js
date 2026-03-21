// ============================================================
// StudySphere - Shared UI & Utility JavaScript
// ============================================================

// ============================================================
// VALIDATION
// ============================================================
function validateEmail(email) {
    // Basic regex for email validation
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    const errors = [];
    if (password.length < 8) errors.push('At least 8 characters required');
    if (!/[A-Z]/.test(password)) errors.push('At least 1 uppercase letter required');
    if (!/[0-9]/.test(password)) errors.push('At least 1 number required');
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) errors.push('At least 1 special character required');
    return errors;
}

// ============================================================
// PASSWORD TOGGLE
// ============================================================
function togglePassword(inputId, btnId) {
    const input = document.getElementById(inputId);
    const btn = document.getElementById(btnId);
    if (!input) return;
    const isHidden = input.type === 'password';
    input.type = isHidden ? 'text' : 'password';
    if (btn) btn.innerHTML = isHidden
        ? `<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21"/></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>`;
}

// ============================================================
// MODAL HELPERS
// ============================================================
function openModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.add('active');
}

function closeModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.remove('active');
}

// Close modal on overlay click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

// ============================================================
// TAB SWITCHING (Dashboards)
// ============================================================
function initTabs(defaultTab) {
    const tabs = document.querySelectorAll('.sidebar-tab[data-tab]');
    const panels = document.querySelectorAll('.tab-panel');

    function activateTab(tabId) {
        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));
        const tab = document.querySelector(`.sidebar-tab[data-tab="${tabId}"]`);
        const panel = document.getElementById('panel-' + tabId);
        if (tab) tab.classList.add('active');
        if (panel) panel.classList.add('active');
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            activateTab(this.getAttribute('data-tab'));
        });
    });

    if (defaultTab) activateTab(defaultTab);
}

// ============================================================
// CALENDAR RENDERER
// ============================================================
const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const DAY_NAMES = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

function renderCalendar(containerId, year, month, slotData, onDayClick) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container._year = year;
    container._month = month;
    container._slotData = slotData;
    container._onDayClick = onDayClick;

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();

    let html = `<div class="flex items-center justify-between mb-4">
        <button type="button" onclick="calNav('${containerId}',-1)" class="p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </button>
        <span class="font-bold text-gray-800">${MONTH_NAMES[month]} ${year}</span>
        <button type="button" onclick="calNav('${containerId}',1)" class="p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </button>
    </div>
    <div class="calendar-grid mb-1">`;

    DAY_NAMES.forEach(d => { html += `<div class="text-center text-xs font-semibold text-gray-400 py-1">${d}</div>`; });
    html += `</div><div class="calendar-grid">`;

    for (let i = 0; i < firstDay; i++) html += `<div class="calendar-day empty"></div>`;

    for (let day = 1; day <= daysInMonth; day++) {
        const ds = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
        const isToday = today.getFullYear()===year && today.getMonth()===month && today.getDate()===day;
        const hasSlot = slotData && slotData[ds] && slotData[ds].length > 0;
        let cls = 'calendar-day';
        if (isToday) cls += ' today';
        else if (hasSlot) cls += ' has-slot';
        html += `<div class="${cls}" onclick="calDayClick('${ds}','${containerId}', event)">${day}</div>`;
    }

    html += `</div>`;
    container.innerHTML = html;
}

function calNav(containerId, delta) {
    const c = document.getElementById(containerId);
    if (!c) return;
    let m = c._month + delta, y = c._year;
    if (m > 11) { m = 0; y++; }
    if (m < 0) { m = 11; y--; }
    renderCalendar(containerId, y, m, c._slotData, c._onDayClick);
}

function calDayClick(ds, containerId, event) {
    document.querySelectorAll(`#${containerId} .calendar-day`).forEach(d => d.classList.remove('selected'));
    if(event && event.target) {
        event.target.classList.add('selected');
    }
    const c = document.getElementById(containerId);
    if (c && c._onDayClick) c._onDayClick(ds);
}
