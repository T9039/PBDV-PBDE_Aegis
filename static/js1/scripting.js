// ============================================================
// StudySphere - Shared JavaScript
// ============================================================

// ============================================================
// MOCK ACCOUNTS
// TODO (Backend): Replace this object with a POST /api/login
//   call that checks credentials against the database.
//   Remove hardcoded passwords before production deployment.
// ============================================================
const ACCOUNTS = {
    'Student1@dut.ac.za': {
        password: 'Student1!',
        role: 'student',
        profile: {
            fullName: 'Sipho Dlamini',
            degreeProgram: 'Bachelor of Science in Computer Science',
            yearOfStudy: '3rd Year',
            learningStyle: 'Visual Learner',
            bio: 'Passionate about technology and software development.'
        }
    },
    'Student2@dut.ac.za': {
        password: 'Student2!',
        role: 'student',
        profile: {
            fullName: 'Nomsa Khumalo',
            degreeProgram: 'Bachelor of Engineering (Electrical)',
            yearOfStudy: '2nd Year',
            learningStyle: 'Auditory Learner',
            bio: 'Eager to learn and grow academically in engineering.'
        }
    },
    'Mentor@dut.ac.za': {
        password: 'Mentor1!',
        role: 'mentor',
        profile: {
            fullName: 'Prof. Thabo Nkosi',
            modules: ['Mathematics', 'Physics', 'Statistics'],
            faculty: 'Faculty of Applied Sciences',
            qualification: 'MSc Mathematics, BSc Honours Physics',
            awards: 'Best Tutor Award 2023, Academic Excellence Award 2022, DUT Outstanding Mentor 2021'
        }
    },
    'Admin@dut.ac.za': {
        password: 'Admin123!',
        role: 'admin',
        profile: { fullName: 'System Administrator' }
    }
};

// ============================================================
// MOCK DATA
// TODO (Backend): Replace all mock data below with actual
//   API calls to the database. Each section is labelled.
// ============================================================

// TODO: GET /api/sessions?user=<email>
const MOCK_SESSIONS = [
    { id: 1, mentorName: 'Prof. Thabo Nkosi', mentorEmail: 'Mentor@dut.ac.za', studentName: 'Sipho Dlamini', studentEmail: 'Student1@dut.ac.za', module: 'Mathematics', date: '2026-03-16', time: '10:00', status: 'booked' },
    { id: 2, mentorName: 'Prof. Thabo Nkosi', mentorEmail: 'Mentor@dut.ac.za', studentName: 'Sipho Dlamini', studentEmail: 'Student1@dut.ac.za', module: 'Physics', date: '2026-03-18', time: '14:00', status: 'booked' },
    { id: 3, mentorName: 'Prof. Thabo Nkosi', mentorEmail: 'Mentor@dut.ac.za', studentName: 'Nomsa Khumalo', studentEmail: 'Student2@dut.ac.za', module: 'Statistics', date: '2026-03-15', time: '09:00', status: 'in-progress' },
    { id: 4, mentorName: 'Prof. Thabo Nkosi', mentorEmail: 'Mentor@dut.ac.za', studentName: 'Sipho Dlamini', studentEmail: 'Student1@dut.ac.za', module: 'Mathematics', date: '2026-03-10', time: '11:00', status: 'cancelled' }
];

// TODO: GET /api/messages?user=<email>
const MOCK_MESSAGES = [
    { id: 1, fromRole: 'mentor', fromName: 'Prof. Thabo Nkosi', fromEmail: 'Mentor@dut.ac.za', toEmail: 'Student1@dut.ac.za', message: 'Focus on Chapter 5 of Calculus — practice integration by parts. Complete exercises 5.1 to 5.3 before our next session.', rating: 'good', date: '2026-03-13' },
    { id: 2, fromRole: 'student', fromName: 'Nomsa Khumalo', fromEmail: 'Student2@dut.ac.za', toEmail: 'Student1@dut.ac.za', message: 'Hey Sipho, want to set up a peer study session for Statistics this week?', date: '2026-03-12' }
];

// TODO: GET /api/mentors
const MOCK_MENTORS = [
    { id: 1, name: 'Prof. Thabo Nkosi', email: 'Mentor@dut.ac.za', faculty: 'Faculty of Applied Sciences', modules: ['Mathematics', 'Physics', 'Statistics'], qualification: 'MSc Mathematics, BSc Honours Physics', awards: 'Best Tutor Award 2023, Academic Excellence Award 2022, DUT Outstanding Mentor 2021', avatar: 'TN', avatarColor: '#003087', sessionsTotal: 48 },
    { id: 2, name: 'Dr. Zanele Mthembu', email: 'zanele.m@dut.ac.za', faculty: 'Faculty of Engineering & Technology', modules: ['Programming', 'Data Structures', 'Algorithms'], qualification: 'PhD Computer Science, MSc Software Engineering', awards: 'Top Tutor 2023, Best Research Assistant 2022', avatar: 'ZM', avatarColor: '#065f46', sessionsTotal: 35 },
    { id: 3, name: 'Mr. Ravi Pillay', email: 'ravi.p@dut.ac.za', faculty: 'Faculty of Accounting & Informatics', modules: ['Accounting', 'Financial Management', 'Economics'], qualification: 'BCom Honours Accounting, CPA', awards: 'Academic Excellence 2021, Faculty Top Student 2020', avatar: 'RP', avatarColor: '#7c2d12', sessionsTotal: 22 }
];

// TODO: GET /api/students
const MOCK_STUDENTS = [
    { id: 1, name: 'Sipho Dlamini', email: 'Student1@dut.ac.za', program: 'BSc Computer Science', year: '3rd Year', avatar: 'SD', avatarColor: '#1e40af' },
    { id: 2, name: 'Nomsa Khumalo', email: 'Student2@dut.ac.za', program: 'BEng Electrical Engineering', year: '2nd Year', avatar: 'NK', avatarColor: '#065f46' }
];

// TODO: GET /api/availability?mentor=<email>
let MENTOR_AVAILABILITY = {
    '2026-03-16': ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00'],
    '2026-03-17': ['09:00', '10:00', '13:00', '14:00'],
    '2026-03-18': ['08:00', '09:00', '14:00', '15:00', '16:00'],
    '2026-03-19': ['10:00', '11:00', '15:00'],
    '2026-03-20': ['09:00', '10:00', '11:00']
};

// TODO: GET /api/mentor-requests (admin)
let PENDING_MENTOR_REQUESTS = [
    { id: 1, name: 'Ms. Priya Singh', email: 'priya.s@dut.ac.za', faculty: 'Faculty of Health Sciences', modules: 'Anatomy, Physiology', qualification: 'BSc Honours Biomedical Science', submittedDate: '2026-03-13', status: 'pending' },
    { id: 2, name: 'Mr. Lethiwe Dube', email: 'lethiwe.d@dut.ac.za', faculty: 'Faculty of Arts & Design', modules: 'Graphic Design, Typography', qualification: 'BDes Visual Communication', submittedDate: '2026-03-12', status: 'pending' }
];

// TODO: GET /api/reports (admin)
const MOCK_REPORTS = [
    { id: 1, from: 'Prof. Thabo Nkosi', fromRole: 'mentor', against: 'Sipho Dlamini', againstRole: 'student', message: 'Student has been consistently late to sessions and not completing assigned work prior to meetings.', date: '2026-03-10', status: 'pending' },
    { id: 2, from: 'Nomsa Khumalo', fromRole: 'student', against: 'Prof. Thabo Nkosi', againstRole: 'mentor', message: 'Mentor cancelled 3 sessions without prior notice this month, affecting my academic progress.', date: '2026-03-11', status: 'pending' }
];

// TODO: Database query for top requested subjects
const COURSE_ANALYTICS = [
    { subject: 'Mathematics', count: 45 },
    { subject: 'Programming', count: 38 },
    { subject: 'Physics', count: 29 }
];

// Peer requests (stored locally for demo)
let peerRequests = JSON.parse(localStorage.getItem('ss_peer_requests') || '[]');
let studentReports = JSON.parse(localStorage.getItem('ss_reports') || '[]');

// ============================================================
// AUTH UTILITIES
// TODO (Backend): Replace sessionStorage with JWT tokens
//   from the backend. Validate tokens server-side.
// ============================================================

function getCurrentUser() {
    return JSON.parse(sessionStorage.getItem('ss_user') || 'null');
}

function setCurrentUser(user) {
    sessionStorage.setItem('ss_user', JSON.stringify(user));
}

function requireAuth(requiredRole) {
    const user = getCurrentUser();
    if (!user) { window.location.href = 'login.html'; return null; }
    if (requiredRole && user.role !== requiredRole) { window.location.href = 'login.html'; return null; }
    return user;
}

function logout() {
    sessionStorage.removeItem('ss_user');
    window.location.href = 'index.html';
}

// ============================================================
// VALIDATION
// ============================================================

function validateEmail(email) {
    return email.includes('@') && email.includes('.');
}

function validatePassword(password) {
    const errors = [];
    if (password.length < 8) errors.push('At least 8 characters required');
    if (!/[A-Z]/.test(password)) errors.push('At least 1 uppercase letter required');
    if (!/[0-9]/.test(password)) errors.push('At least 1 number required');
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) errors.push('At least 1 special character required (e.g. ! @ # $)');
    return errors;
}

function showFieldError(inputEl, errorEl, message) {
    if (inputEl) inputEl.classList.add('error');
    if (errorEl) errorEl.textContent = message;
}

function clearFieldError(inputEl, errorEl) {
    if (inputEl) inputEl.classList.remove('error');
    if (errorEl) errorEl.textContent = '';
}

// ============================================================
// FLASH MESSAGES
// ============================================================

function showFlash(message, type = 'success') {
    const old = document.querySelector('.flash-message');
    if (old) old.remove();

    const colors = {
        success: 'background:#d1fae5;color:#065f46;border:1px solid #a7f3d0;',
        error: 'background:#fee2e2;color:#dc2626;border:1px solid #fecaca;',
        info: 'background:#dbeafe;color:#1e40af;border:1px solid #bfdbfe;',
        warning: 'background:#fef3c7;color:#92400e;border:1px solid #fde68a;'
    };

    const el = document.createElement('div');
    el.className = 'flash-message';
    el.style.cssText = colors[type] || colors.success;
    el.textContent = message;
    document.body.appendChild(el);

    setTimeout(() => {
        el.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => el.remove(), 300);
    }, 4000);
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
        <button onclick="calNav('${containerId}',-1)" class="p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </button>
        <span class="font-bold text-gray-800">${MONTH_NAMES[month]} ${year}</span>
        <button onclick="calNav('${containerId}',1)" class="p-2 rounded-lg hover:bg-gray-100 transition-colors">
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
        html += `<div class="${cls}" onclick="calDayClick('${ds}','${containerId}')">${day}</div>`;
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

function calDayClick(ds, containerId) {
    // Highlight selected day
    document.querySelectorAll(`#${containerId} .calendar-day`).forEach(d => d.classList.remove('selected'));
    event.target.classList.add('selected');

    const c = document.getElementById(containerId);
    if (c && c._onDayClick) c._onDayClick(ds);
}
