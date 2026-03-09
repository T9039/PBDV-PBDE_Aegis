// ===================== MOCK DATA =====================
const mockMentors = [
  {
    id: 1, name: "Dr. Sarah Johnson", faculty: "Faculty of Engineering",
    subjects: ["Mathematics", "Calculus", "Statistics"],
    qualifications: "BSc Mathematics (Hons), MSc Applied Mathematics, PhD Computational Mathematics",
    awards: ["Best Mentor Award 2024", "Dean's Excellence Award 2023"],
    bio: "Passionate about making mathematics accessible and enjoyable for all students.",
    initials: "SJ",
    availability: {
      "2026-03-10": ["09:00 - 10:00", "11:00 - 12:00", "14:00 - 15:00"],
      "2026-03-12": ["10:00 - 11:00", "13:00 - 14:00"],
      "2026-03-16": ["09:00 - 10:00", "15:00 - 16:00"],
      "2026-03-18": ["11:00 - 12:00", "14:00 - 15:00"],
      "2026-03-23": ["09:00 - 10:00", "10:00 - 11:00"],
    }
  },
  {
    id: 2, name: "Prof. Michael Dlamini", faculty: "Faculty of ICT",
    subjects: ["Programming", "Data Structures", "Web Development"],
    qualifications: "BSc Computer Science, MSc Software Engineering, PhD Distributed Systems",
    awards: ["Top Mentor 2025", "Student Choice Award 2024"],
    bio: "Software engineer turned educator with 12 years of industry experience.",
    initials: "MD",
    availability: {
      "2026-03-11": ["08:00 - 09:00", "10:00 - 11:00", "14:00 - 15:00"],
      "2026-03-13": ["09:00 - 10:00", "11:00 - 12:00"],
      "2026-03-17": ["10:00 - 11:00", "13:00 - 14:00"],
      "2026-03-20": ["09:00 - 10:00", "15:00 - 16:00"],
    }
  },
  {
    id: 3, name: "Ms. Priya Naidoo", faculty: "Faculty of Management Sciences",
    subjects: ["Accounting", "Financial Management", "Business Statistics"],
    qualifications: "BCom Accounting (Hons), MCom Financial Management, CA(SA) in progress",
    awards: ["Emerging Mentor Award 2025"],
    bio: "Dedicated to helping students understand the practical side of finance and accounting.",
    initials: "PN",
    availability: {
      "2026-03-10": ["10:00 - 11:00", "13:00 - 14:00"],
      "2026-03-14": ["09:00 - 10:00", "11:00 - 12:00", "15:00 - 16:00"],
      "2026-03-19": ["10:00 - 11:00", "14:00 - 15:00"],
      "2026-03-24": ["09:00 - 10:00", "11:00 - 12:00"],
    }
  },
  {
    id: 4, name: "Mr. Thabo Khumalo", faculty: "Faculty of Applied Sciences",
    subjects: ["Physics", "Thermodynamics", "Fluid Mechanics"],
    initials: "TK", awards: [],
    qualifications: "BSc Physics, MSc Mechanical Engineering",
    bio: "Physics enthusiast helping engineering students master their fundamentals.",
    availability: {
      "2026-03-11": ["09:00 - 10:00", "13:00 - 14:00"],
      "2026-03-16": ["10:00 - 11:00", "14:00 - 15:00"],
      "2026-03-18": ["09:00 - 10:00"],
    }
  }
];

const mockStudents = [
  { id: 101, name: "Lungelo Ndaba", email: "lungelo@dut.ac.za", module: "Mathematics", sessions: 8 },
  { id: 102, name: "Ayesha Patel", email: "ayesha@dut.ac.za", module: "Programming", sessions: 5 },
  { id: 103, name: "Ryan Smith", email: "ryan@dut.ac.za", module: "Accounting", sessions: 11 },
  { id: 104, name: "Nomvula Zulu", email: "nomvula@dut.ac.za", module: "Physics", sessions: 3 },
];

const mockStudentMessages = [
  { id: 1, mentorId: 1, mentorName: "Dr. Sarah Johnson", message: "Great progress on integration! Focus on Chapter 7 - Taylor Series, and complete exercises 7.1 to 7.5 before our next session.", rating: "Excellent", date: "2026-03-07" },
  { id: 2, mentorId: 2, mentorName: "Prof. Michael Dlamini", message: "Your linked list implementation is mostly correct. Review pointer management and run the test suite I shared.", rating: "Good", date: "2026-03-05" },
];

const mockUpcomingSessions = [
  { id: 1, mentor: "Dr. Sarah Johnson", module: "Mathematics - Calculus", date: "2026-03-11", time: "09:00 - 10:00", status: "Booked" },
  { id: 2, mentor: "Prof. Michael Dlamini", module: "Programming - Data Structures", date: "2026-03-13", time: "10:00 - 11:00", status: "In Progress" },
  { id: 3, mentor: "Ms. Priya Naidoo", module: "Accounting", date: "2026-03-14", time: "11:00 - 12:00", status: "Booked" },
];

const mockMentorBookings = [
  { id: 1, student: "Lungelo Ndaba", studentId: 101, module: "Mathematics - Integration", date: "2026-03-11", time: "09:00 - 10:00", status: "Booked" },
  { id: 2, student: "Ayesha Patel", studentId: 102, module: "Mathematics - Series", date: "2026-03-12", time: "11:00 - 12:00", status: "Booked" },
  { id: 3, student: "Ryan Smith", studentId: 103, module: "Statistics", date: "2026-03-16", time: "09:00 - 10:00", status: "In Progress" },
];

const mockMentorSessions = [
  { id: 1, studentId: 101, studentName: "Lungelo Ndaba", module: "Mathematics - Integration", date: "2026-03-07", qualification: "BSc Engineering Y2", hasMessage: true, rating: "Excellent" },
  { id: 2, studentId: 102, studentName: "Ayesha Patel", module: "Mathematics - Derivatives", date: "2026-03-04", qualification: "BSc Computer Science Y1", hasMessage: false, rating: "" },
  { id: 3, studentId: 103, studentName: "Ryan Smith", module: "Statistics - Probability", date: "2026-03-01", qualification: "BCom Accounting Y3", hasMessage: true, rating: "Good" },
];

const mockFeedback = [
  { id: 1, studentName: "Lungelo Ndaba", rating: 5, review: "Excellent explanations, very patient and helpful. Always well-prepared.", date: "2026-03-08" },
  { id: 2, studentName: "Ryan Smith", rating: 4, review: "Very knowledgeable. Sessions are structured and productive.", date: "2026-03-06" },
];

const mockQueries = [
  { id: 1, from: "Prof. Michael Dlamini", about: "Student: Ryan Smith", type: "mentor-report", message: "Student was repeatedly disrespectful during the session and failed to complete agreed preparatory work. Request admin review.", date: "2026-03-08" },
  { id: 2, from: "Nomvula Zulu (Student)", about: "Mentor: Mr. Thabo Khumalo", type: "student-report", message: "Mentor cancelled two consecutive sessions without prior notice which affected my exam preparation.", date: "2026-03-07" },
];

const mockMentorRequests = [
  { id: 1, name: "Sipho Mthethwa", email: "sipho@dut.ac.za", faculty: "Faculty of Engineering", subjects: "Structural Analysis, Civil Engineering", qualifications: "BSc Civil Engineering (Hons)" },
  { id: 2, name: "Fatima Cassim", email: "fatima@dut.ac.za", faculty: "Faculty of ICT", subjects: "Cybersecurity, Networking", qualifications: "BSc Information Technology, CISSP" },
];

const mockAllUsers = [
  { id: 101, name: "Lungelo Ndaba", role: "student", module: "Mathematics", status: "Active" },
  { id: 102, name: "Ayesha Patel", role: "student", module: "Programming", status: "Active" },
  { id: 103, name: "Ryan Smith", role: "student", module: "Accounting", status: "Active" },
  { id: 104, name: "Nomvula Zulu", role: "student", module: "Physics", status: "Active" },
  { id: 1, name: "Dr. Sarah Johnson", role: "mentor", module: "Mathematics, Calculus", status: "Active" },
  { id: 2, name: "Prof. Michael Dlamini", role: "mentor", module: "Programming, Data Structures", status: "Active" },
  { id: 3, name: "Ms. Priya Naidoo", role: "mentor", module: "Accounting, Finance", status: "Active" },
  { id: 4, name: "Mr. Thabo Khumalo", role: "mentor", module: "Physics, Thermodynamics", status: "Active" },
];

// ===================== STATE =====================
let currentUser = null;
let currentRole = null;
let currentMentorId = null;
let selectedBookingDate = null;
let selectedBookingSlot = null;
let selectedMessageStudentId = null;
let studentRating = 0;
let bookedSessions = [...mockUpcomingSessions];
let mentorRequests = [...mockMentorRequests];
let queries = [...mockQueries];
let feedback = [...mockFeedback];
let allUsers = [...mockAllUsers];

// ===================== PAGE / TAB SWITCHING =====================
function showPage(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const page = document.getElementById(pageId);
  if (page) page.classList.add('active');
}

function switchTab(dashboard, tabName, btn) {
  const prefix = dashboard === 'student' ? 'student' : dashboard === 'mentor' ? 'mentor' : 'admin';
  document.querySelectorAll(`#${prefix}-dashboard .tab-content`).forEach(t => t.classList.remove('active'));
  document.querySelectorAll(`#${prefix}-dashboard .nav-btn`).forEach(b => b.classList.remove('active'));
  const tab = document.getElementById(`${prefix}-${tabName}`);
  if (tab) tab.classList.add('active');
  if (btn) btn.classList.add('active');

  // Lazy-render content on first open
  if (dashboard === 'student' && tabName === 'home') renderStudentHome();
  if (dashboard === 'student' && tabName === 'search') renderMentorResults(mockMentors);
  if (dashboard === 'student' && tabName === 'feedback') populateFeedbackMentors();
  if (dashboard === 'mentor' && tabName === 'home') renderMentorHome();
  if (dashboard === 'mentor' && tabName === 'availability') renderMentorCalendar();
  if (dashboard === 'mentor' && tabName === 'messages') renderMentorMessages();
  if (dashboard === 'mentor' && tabName === 'feedback') renderMentorFeedback();
  if (dashboard === 'admin' && tabName === 'users') renderUsersTable(allUsers);
  if (dashboard === 'admin' && tabName === 'analytics') renderBarChart();
  if (dashboard === 'admin' && tabName === 'queries') renderQueries();
  if (dashboard === 'admin' && tabName === 'manage') renderManageUsers();
}

// ===================== AUTH =====================
function showLoginModal(role) {
  document.getElementById('login-role').value = role;
  document.getElementById('login-modal-title').textContent =
    role === 'student' ? 'Student Login' : role === 'mentor' ? 'Mentor Login' : 'Admin Login';
  document.getElementById('login-modal').style.display = 'flex';
}

function showSignupModal() {
  document.getElementById('signup-modal').style.display = 'flex';
}

function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}

function toggleMentorFields() {
  const role = document.getElementById('signup-role').value;
  document.getElementById('mentor-signup-fields').style.display = role === 'mentor' ? 'block' : 'none';
}

function handleLogin(e) {
  e.preventDefault();
  const role = document.getElementById('login-role').value;
  closeModal('login-modal');

  if (role === 'student') {
    currentUser = { name: "John Student", initials: "JS" };
    document.getElementById('student-name-display').textContent = currentUser.name;
    document.getElementById('student-avatar').textContent = currentUser.initials;
    showPage('student-dashboard');
    renderStudentHome();
    populateFeedbackMentors();
  } else if (role === 'mentor') {
    currentUser = { name: "Dr. Sarah Johnson", initials: "SJ" };
    document.getElementById('mentor-name-display').textContent = currentUser.name;
    document.getElementById('mentor-avatar').textContent = currentUser.initials;
    showPage('mentor-dashboard');
    renderMentorHome();
  } else if (role === 'admin') {
    currentUser = { name: "Admin", initials: "AD" };
    showPage('admin-dashboard');
  }
  showToast('Welcome back!', 'success');
}

function handleSignup(e) {
  e.preventDefault();
  const name = document.getElementById('signup-name').value;
  const role = document.getElementById('signup-role').value;
  closeModal('signup-modal');
  if (role === 'mentor') {
    showToast(`Your mentor request has been submitted, ${name}. Await admin approval.`, 'warning');
    // In real app: send to backend + email notification
    simulateEmail(document.getElementById('signup-email').value, 'pending');
  } else {
    showToast(`Account created! Welcome, ${name}. You may now log in.`, 'success');
  }
}

function logout() {
  currentUser = null;
  showPage('landing-page');
  showToast('You have been logged out.', 'success');
}

// ===================== STUDENT HOME =====================
function renderStudentHome() {
  // Messages
  const msgList = document.getElementById('student-messages-list');
  if (!msgList) return;
  msgList.innerHTML = '';
  if (mockStudentMessages.length === 0) {
    msgList.innerHTML = '<div class="empty-state"><p>No messages yet.</p></div>';
    return;
  }
  mockStudentMessages.forEach(msg => {
    const ratingClass = getRatingClass(msg.rating);
    msgList.innerHTML += `
      <div class="message-item" onclick="openMessageThread(${msg.mentorId}, '${msg.mentorName}')">
        <div class="message-info">
          <h4>${msg.mentorName}</h4>
          <p>${msg.message.substring(0, 60)}...</p>
          <p style="margin-top:4px;font-size:0.75rem;color:#5a7a9a">${msg.date}</p>
        </div>
        <span class="rating-badge ${ratingClass}">${msg.rating}</span>
      </div>`;
  });

  // Sessions
  const sesList = document.getElementById('student-sessions-list');
  sesList.innerHTML = '';
  bookedSessions.forEach(s => {
    sesList.innerHTML += `
      <div class="session-item">
        <div class="session-info">
          <h4>${s.module}</h4>
          <p>${s.mentor}</p>
          <p>${s.date} &bull; ${s.time}</p>
        </div>
        <div class="session-meta">
          <span class="status-badge ${getStatusClass(s.status)}">${s.status}</span>
          <button class="btn btn-sm btn-danger" onclick="cancelSession(${s.id})">Cancel</button>
        </div>
      </div>`;
  });
  if (bookedSessions.length === 0) sesList.innerHTML = '<div class="empty-state"><p>No upcoming sessions.</p></div>';
  document.getElementById('s-sessions-week').textContent = bookedSessions.length;
}

function cancelSession(id) {
  bookedSessions = bookedSessions.filter(s => s.id !== id);
  renderStudentHome();
  showToast('Session cancelled.', 'warning');
}

function openMessageThread(mentorId, mentorName) {
  document.getElementById('thread-mentor-name').textContent = `Messages from ${mentorName}`;
  const msgs = mockStudentMessages.filter(m => m.mentorId === mentorId);
  const container = document.getElementById('thread-content');
  container.innerHTML = '';
  msgs.forEach(m => {
    container.innerHTML += `
      <div class="thread-bubble from-mentor">
        <p>${m.message}</p>
        <div class="bubble-meta">${m.date} &bull; Rating: <strong>${m.rating}</strong></div>
      </div>`;
  });
  document.getElementById('message-thread-modal').style.display = 'flex';
}

// ===================== SEARCH MENTORS =====================
function searchMentors() {
  const query = document.getElementById('search-input').value.toLowerCase().trim();
  const type = document.getElementById('search-type').value;
  if (!query) { renderMentorResults(mockMentors); return; }
  const filtered = mockMentors.filter(m => {
    if (type === 'name') return m.name.toLowerCase().includes(query);
    return m.subjects.some(s => s.toLowerCase().includes(query));
  });
  renderMentorResults(filtered);
}

function renderMentorResults(mentors) {
  const container = document.getElementById('mentor-results');
  if (!container) return;
  if (mentors.length === 0) {
    container.innerHTML = '<div class="empty-state" style="grid-column:1/-1"><p>No mentors found. Try a different search.</p></div>';
    return;
  }
  container.innerHTML = mentors.map(m => `
    <div class="mentor-card">
      <div class="mentor-card-header">
        <div class="mentor-avatar">${m.initials}</div>
        <div>
          <h4>${m.name}</h4>
          <p>${m.faculty}</p>
        </div>
      </div>
      <div class="mentor-subjects">
        ${m.subjects.map(s => `<span class="subject-tag">${s}</span>`).join('')}
      </div>
      <div class="mentor-card-actions">
        <button class="btn btn-sm btn-ghost" onclick="viewMentorProfile(${m.id})">View Profile</button>
        <button class="btn btn-sm btn-primary" onclick="openBookSession(${m.id})">Book Session</button>
      </div>
    </div>`).join('');
}

function viewMentorProfile(mentorId) {
  const m = mockMentors.find(x => x.id === mentorId);
  if (!m) return;
  currentMentorId = mentorId;
  const awardsHtml = m.awards.length
    ? `<ul>${m.awards.map(a => `<li>${a}</li>`).join('')}</ul>`
    : '<p>No awards listed.</p>';
  document.getElementById('mentor-profile-content').innerHTML = `
    <div class="profile-header">
      <div class="profile-avatar">${m.initials}</div>
      <div>
        <h2>${m.name}</h2>
        <p>${m.faculty}</p>
      </div>
    </div>
    <div class="profile-section">
      <h4>About</h4>
      <p>${m.bio}</p>
    </div>
    <div class="profile-section">
      <h4>Qualifications</h4>
      <p>${m.qualifications}</p>
    </div>
    <div class="profile-section">
      <h4>Subjects Taught</h4>
      <div class="mentor-subjects">${m.subjects.map(s => `<span class="subject-tag">${s}</span>`).join('')}</div>
    </div>
    <div class="profile-section">
      <h4>Awards &amp; Recognition</h4>
      ${awardsHtml}
    </div>`;
  document.getElementById('mentor-profile-modal').style.display = 'flex';
}

function openBookSession(mentorId) {
  currentMentorId = mentorId;
  closeModal('mentor-profile-modal');
  selectedBookingDate = null;
  selectedBookingSlot = null;
  renderBookingCalendar(mentorId);
  document.getElementById('available-slots').innerHTML = '<p class="muted">Pick a date first.</p>';
  document.getElementById('booking-notes').value = '';
  document.getElementById('book-session-modal').style.display = 'flex';
}

function renderBookingCalendar(mentorId) {
  const mentor = mockMentors.find(m => m.id === mentorId);
  const container = document.getElementById('booking-calendar');
  container.innerHTML = '';
  const days = ['Su','Mo','Tu','We','Th','Fr','Sa'];
  days.forEach(d => container.innerHTML += `<div class="cal-header">${d}</div>`);
  const year = 2026, month = 2; // March
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  for (let i = 0; i < firstDay; i++) container.innerHTML += `<div class="cal-day empty"></div>`;
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `2026-03-${String(d).padStart(2,'0')}`;
    const hasSlots = mentor && mentor.availability[dateStr];
    const isToday = d === 9;
    const div = document.createElement('div');
    div.className = `cal-day${hasSlots ? ' has-booking' : ''}${isToday ? ' today' : ''}`;
    div.textContent = d;
    if (hasSlots) div.onclick = () => selectBookingDate(dateStr, mentor, div);
    container.appendChild(div);
  }
}

function selectBookingDate(dateStr, mentor, el) {
  selectedBookingDate = dateStr;
  document.querySelectorAll('#booking-calendar .cal-day').forEach(d => d.classList.remove('selected'));
  el.classList.add('selected');
  const slots = mentor.availability[dateStr] || [];
  const container = document.getElementById('available-slots');
  container.innerHTML = '';
  slots.forEach(slot => {
    const div = document.createElement('div');
    div.className = 'slot-item';
    div.textContent = slot;
    div.onclick = () => {
      document.querySelectorAll('#available-slots .slot-item').forEach(s => s.classList.remove('selected'));
      div.classList.add('selected');
      selectedBookingSlot = slot;
    };
    container.appendChild(div);
  });
  if (slots.length === 0) container.innerHTML = '<p class="muted">No slots available on this date.</p>';
}

function confirmBooking() {
  if (!selectedBookingDate || !selectedBookingSlot) {
    showToast('Please select a date and time slot.', 'warning');
    return;
  }
  const mentor = mockMentors.find(m => m.id === currentMentorId);
  const notes = document.getElementById('booking-notes').value;
  const newSession = {
    id: Date.now(), mentor: mentor.name,
    module: mentor.subjects[0], date: selectedBookingDate,
    time: selectedBookingSlot, status: "Booked", notes
  };
  bookedSessions.push(newSession);
  closeModal('book-session-modal');
  showToast(`Session booked with ${mentor.name} on ${selectedBookingDate} at ${selectedBookingSlot}!`, 'success');
  renderStudentHome();
}

// ===================== STUDENT FEEDBACK =====================
function populateFeedbackMentors() {
  const sel = document.getElementById('feedback-mentor-select');
  if (!sel) return;
  sel.innerHTML = '<option value="">-- Select a mentor --</option>';
  mockMentors.forEach(m => sel.innerHTML += `<option value="${m.id}">${m.name}</option>`);
}

function setRating(val) {
  studentRating = val;
  document.getElementById('feedback-rating').value = val;
  document.querySelectorAll('#star-rating span').forEach((s, i) => {
    s.classList.toggle('active', i < val);
  });
}

function submitStudentFeedback(e) {
  e.preventDefault();
  const mentorId = document.getElementById('feedback-mentor-select').value;
  const text = document.getElementById('feedback-text').value;
  if (!mentorId) { showToast('Please select a mentor.', 'warning'); return; }
  if (studentRating === 0) { showToast('Please select a rating.', 'warning'); return; }
  if (!text.trim()) { showToast('Please write a review.', 'warning'); return; }
  feedback.push({ id: Date.now(), studentName: "John Student", rating: studentRating, review: text, date: new Date().toISOString().slice(0,10) });
  document.getElementById('feedback-text').value = '';
  document.getElementById('feedback-mentor-select').value = '';
  setRating(0);
  showToast('Feedback submitted! Thank you.', 'success');
}

// ===================== MENTOR HOME =====================
function renderMentorHome() {
  const list = document.getElementById('mentor-bookings-list');
  if (!list) return;
  list.innerHTML = '';
  mockMentorBookings.forEach(b => {
    list.innerHTML += `
      <div class="session-item">
        <div class="session-info">
          <h4>${b.student}</h4>
          <p>${b.module} &bull; ${b.date} &bull; ${b.time}</p>
        </div>
        <div class="session-meta">
          <span class="status-badge ${getStatusClass(b.status)}">${b.status}</span>
          <button class="btn btn-sm btn-ghost" onclick="viewStudentDetail(${b.studentId})">View Details</button>
          <button class="btn btn-sm btn-danger" onclick="cancelMentorBooking(${b.id})">Cancel</button>
        </div>
      </div>`;
  });
  if (mockMentorBookings.length === 0) list.innerHTML = '<div class="empty-state"><p>No upcoming bookings.</p></div>';
  document.getElementById('m-sessions-week').textContent = mockMentorBookings.length;
}

function cancelMentorBooking(id) {
  const idx = mockMentorBookings.findIndex(b => b.id === id);
  if (idx > -1) mockMentorBookings.splice(idx, 1);
  renderMentorHome();
  showToast('Booking cancelled.', 'warning');
}

function viewStudentDetail(studentId) {
  const s = mockStudents.find(x => x.id === studentId);
  if (!s) return;
  const sessions = mockMentorSessions.filter(m => m.studentId === studentId);
  document.getElementById('student-detail-content').innerHTML = `
    <h2>${s.name}</h2>
    <p style="color:#7a9cc0;margin:6px 0 20px">${s.module} &bull; ${s.email}</p>
    <div class="profile-section">
      <h4>Session History with You</h4>
      <p>Previous sessions: <strong>${sessions.length}</strong></p>
    </div>
    <div class="profile-section">
      <h4>Recent Sessions</h4>
      ${sessions.map(ses => `
        <div style="padding:10px;background:rgba(255,255,255,0.04);border-radius:8px;margin-bottom:8px">
          <strong style="color:#c0d8f0">${ses.module}</strong><br>
          <span style="color:#7a9cc0;font-size:0.82rem">${ses.date}</span>
          ${ses.rating ? `<span class="rating-badge ${getRatingClass(ses.rating)}" style="float:right">${ses.rating}</span>` : ''}
        </div>`).join('')}
    </div>`;
  selectedMessageStudentId = studentId;
  document.getElementById('student-detail-modal').style.display = 'flex';
}

function reportStudent() {
  const s = mockStudents.find(x => x.id === selectedMessageStudentId);
  closeModal('student-detail-modal');
  if (s) {
    queries.push({
      id: Date.now(), from: "Dr. Sarah Johnson", about: `Student: ${s.name}`,
      type: "mentor-report", message: "Conduct issue reported by mentor. Please review.",
      date: new Date().toISOString().slice(0,10)
    });
    showToast(`Report sent to admin regarding ${s.name}.`, 'warning');
  }
}

// ===================== MENTOR AVAILABILITY =====================
function renderMentorCalendar() {
  const container = document.getElementById('mentor-calendar');
  if (!container) return;
  container.innerHTML = '';
  const days = ['Su','Mo','Tu','We','Th','Fr','Sa'];
  days.forEach(d => container.innerHTML += `<div class="cal-header">${d}</div>`);
  const firstDay = new Date(2026, 2, 1).getDay();
  const daysInMonth = 31;
  const mentor = mockMentors[0];
  for (let i = 0; i < firstDay; i++) container.innerHTML += `<div class="cal-day empty"></div>`;
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `2026-03-${String(d).padStart(2,'0')}`;
    const hasSlots = mentor.availability[dateStr];
    const div = document.createElement('div');
    div.className = `cal-day${hasSlots ? ' has-booking' : ''}${d === 9 ? ' today' : ''}`;
    div.textContent = d;
    if (hasSlots) {
      div.onclick = () => {
        document.querySelectorAll('#mentor-calendar .cal-day').forEach(x => x.classList.remove('selected'));
        div.classList.add('selected');
        document.getElementById('mentor-selected-date').textContent = `Slots for ${dateStr}`;
        const slotsEl = document.getElementById('mentor-slots');
        slotsEl.innerHTML = '';
        mentor.availability[dateStr].forEach(slot => {
          slotsEl.innerHTML += `<div class="slot-item">${slot}</div>`;
        });
      };
    }
    container.appendChild(div);
  }
}

// ===================== MENTOR MESSAGES =====================
function renderMentorMessages() {
  const container = document.getElementById('mentor-sessions-msg-list');
  if (!container) return;
  container.innerHTML = '';
  mockMentorSessions.forEach(s => {
    container.innerHTML += `
      <div class="session-msg-card">
        <div class="session-msg-card-header">
          <div>
            <h4>${s.studentName}</h4>
            <p>${s.module} &bull; ${s.date} &bull; ${s.qualification}</p>
          </div>
          ${s.rating ? `<span class="rating-badge ${getRatingClass(s.rating)}">${s.rating}</span>` : ''}
        </div>
        <button class="btn btn-sm btn-primary" onclick="openAddMessage(${s.studentId})">Add Message</button>
        ${s.hasMessage ? `<span style="margin-left:10px;color:#1abc9c;font-size:0.8rem">&#10003; Message sent</span>` : ''}
      </div>`;
  });
}

function openAddMessage(studentId) {
  selectedMessageStudentId = studentId;
  document.getElementById('msg-student-id').value = studentId;
  document.getElementById('performance-rating').value = '';
  document.getElementById('mentor-message-text').value = '';
  document.getElementById('add-message-modal').style.display = 'flex';
}

function sendMentorMessage() {
  const rating = document.getElementById('performance-rating').value;
  const text = document.getElementById('mentor-message-text').value;
  if (!rating) { showToast('Please select a performance rating.', 'warning'); return; }
  if (!text.trim()) { showToast('Please write a message.', 'warning'); return; }
  const s = mockMentorSessions.find(x => x.studentId === selectedMessageStudentId);
  if (s) { s.hasMessage = true; s.rating = rating; }
  mockStudentMessages.push({
    id: Date.now(), mentorId: 1, mentorName: "Dr. Sarah Johnson",
    message: text, rating: rating, date: new Date().toISOString().slice(0,10)
  });
  closeModal('add-message-modal');
  renderMentorMessages();
  showToast('Message sent to student!', 'success');
}

// ===================== MENTOR FEEDBACK =====================
function renderMentorFeedback() {
  const container = document.getElementById('mentor-feedback-list');
  if (!container) return;
  if (feedback.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No feedback received yet.</p></div>';
    return;
  }
  container.innerHTML = feedback.map(f => `
    <div class="feedback-card">
      <div class="feedback-card-header">
        <strong>${f.studentName}</strong>
        <span class="star-display">${'&#9733;'.repeat(f.rating)}${'&#9734;'.repeat(5 - f.rating)}</span>
      </div>
      <p>${f.review}</p>
      <p style="font-size:0.76rem;color:#5a7a9a;margin-top:8px">${f.date}</p>
    </div>`).join('');
}

// ===================== ADMIN =====================
function renderUsersTable(users) {
  const tbody = document.getElementById('users-table-body');
  if (!tbody) return;
  tbody.innerHTML = users.map(u => `
    <tr>
      <td>${u.name}</td>
      <td><span style="text-transform:capitalize;color:${u.role==='mentor'?'#d4af37':'#4ba3e8'}">${u.role}</span></td>
      <td>${u.module}</td>
      <td><span class="status-badge status-booked">${u.status}</span></td>
      <td><button class="btn btn-sm btn-danger" onclick="removeUserAdmin(${u.id},'${u.role}')">Remove</button></td>
    </tr>`).join('');
}

function filterUsers() {
  const type = document.getElementById('user-type-filter').value;
  const query = document.getElementById('user-search').value.toLowerCase();
  let filtered = allUsers;
  if (type !== 'all') filtered = filtered.filter(u => u.role === type);
  if (query) filtered = filtered.filter(u =>
    u.name.toLowerCase().includes(query) ||
    u.module.toLowerCase().includes(query)
  );
  renderUsersTable(filtered);
}

function removeUserAdmin(id, role) {
  const user = allUsers.find(u => u.id === id && u.role === role);
  if (!user) return;
  allUsers = allUsers.filter(u => !(u.id === id && u.role === role));
  filterUsers();
  showToast(`${user.name} has been removed. Notification email sent.`, 'warning');
  simulateEmail(user.name, 'removed');
}

function renderBarChart() {
  const data = [
    { subject: "Mathematics", count: 58, pct: 100, barClass: "bar-1" },
    { subject: "Programming", count: 43, pct: 74, barClass: "bar-2" },
    { subject: "Accounting", count: 37, pct: 64, barClass: "bar-3" },
  ];
  const container = document.getElementById('bar-chart-container');
  if (!container) return;
  container.innerHTML = data.map(d => `
    <div class="bar-row">
      <div class="bar-label">${d.subject}</div>
      <div class="bar-track">
        <div class="bar-fill ${d.barClass}" style="width:${d.pct}%">${d.count} students</div>
      </div>
    </div>`).join('');
}

function renderQueries() {
  const container = document.getElementById('queries-list');
  if (!container) return;
  if (queries.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No queries at this time.</p></div>';
    return;
  }
  container.innerHTML = queries.map(q => `
    <div class="query-card unread">
      <div class="query-header">
        <div>
          <strong>${q.from}</strong> &mdash;
          <span style="color:#7a9cc0">${q.about}</span>
          <span class="query-type ${q.type === 'mentor-report' ? 'query-mentor-report' : 'query-student-report'}" style="margin-left:8px">
            ${q.type === 'mentor-report' ? 'Mentor Report' : 'Student Report'}
          </span>
        </div>
        <span>${q.date}</span>
      </div>
      <p>${q.message}</p>
    </div>`).join('');
}

function renderManageUsers() {
  // Mentor requests
  const reqContainer = document.getElementById('mentor-requests-list');
  if (reqContainer) {
    if (mentorRequests.length === 0) {
      reqContainer.innerHTML = '<p class="muted">No pending requests.</p>';
    } else {
      reqContainer.innerHTML = mentorRequests.map(r => `
        <div class="request-item">
          <div class="request-info">
            <h4>${r.name}</h4>
            <p>${r.faculty} &bull; ${r.subjects}</p>
            <p style="margin-top:2px">${r.qualifications}</p>
          </div>
          <div class="request-actions">
            <button class="btn btn-sm btn-signup" onclick="approveMentor(${r.id})">Approve</button>
            <button class="btn btn-sm btn-danger" onclick="rejectMentor(${r.id})">Reject</button>
          </div>
        </div>`).join('');
    }
  }
  filterRemoveUsers();
}

function approveMentor(id) {
  const req = mentorRequests.find(r => r.id === id);
  if (!req) return;
  mentorRequests = mentorRequests.filter(r => r.id !== id);
  allUsers.push({ id: Date.now(), name: req.name, role: 'mentor', module: req.subjects, status: 'Active' });
  renderManageUsers();
  showToast(`${req.name} approved as mentor. Notification email sent.`, 'success');
  simulateEmail(req.email, 'approved');
}

function rejectMentor(id) {
  const req = mentorRequests.find(r => r.id === id);
  if (!req) return;
  mentorRequests = mentorRequests.filter(r => r.id !== id);
  renderManageUsers();
  showToast(`${req.name}'s request has been rejected.`, 'warning');
}

function filterRemoveUsers() {
  const query = document.getElementById('remove-search')?.value.toLowerCase() || '';
  const container = document.getElementById('remove-users-list');
  if (!container) return;
  const filtered = query ? allUsers.filter(u => u.name.toLowerCase().includes(query)) : allUsers;
  container.innerHTML = filtered.slice(0, 10).map(u => `
    <div class="remove-user-item">
      <span>${u.name}<small>(${u.role})</small></span>
      <button class="btn btn-sm btn-danger" onclick="removeUserAdmin(${u.id},'${u.role}')">Remove</button>
    </div>`).join('');
  if (filtered.length === 0) container.innerHTML = '<p class="muted">No users found.</p>';
}

// ===================== HELPERS =====================
function getRatingClass(rating) {
  if (!rating) return '';
  const r = rating.toLowerCase();
  if (r.includes('excellent')) return 'rating-excellent';
  if (r.includes('good')) return 'rating-good';
  if (r.includes('moderate')) return 'rating-moderate';
  return 'rating-attention';
}

function getStatusClass(status) {
  if (!status) return '';
  const s = status.toLowerCase();
  if (s.includes('progress')) return 'status-inprogress';
  if (s.includes('cancel')) return 'status-cancelled';
  return 'status-booked';
}

function showToast(msg, type = 'info') {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = `toast show ${type}`;
  setTimeout(() => toast.className = 'toast', 4000);
}

// Simulated Email API
function simulateEmail(emailOrName, action) {
  let subject = '', body = '';
  if (action === 'approved') {
    subject = 'Your Mentor Application Has Been Approved';
    body = `Greetings ma'am/sir, hope you are well. Your request has been approved. We look forward to working with you in our DUT Mentorship Platform.`;
  } else if (action === 'removed') {
    subject = 'Account Removal Notification';
    body = `Greetings ma'am/sir, hope you are well. We would like to inform you that your account on the DUT Mentorship Platform has been removed. If you believe this is in error, please contact the platform administrator.`;
  } else if (action === 'pending') {
    subject = 'Mentor Application Received';
    body = `Greetings ma'am/sir, hope you are well. Your mentor application has been received and is pending admin approval. We will notify you once a decision has been made.`;
  }
  // In production: replace with actual Email API call (e.g. EmailJS or backend endpoint)
  console.log(`[Email API] To: ${emailOrName} | Subject: ${subject} | Body: ${body}`);
}

// ===================== INIT =====================
document.addEventListener('DOMContentLoaded', () => {
  // Show landing page by default
  showPage('landing-page');

  // Close modals when clicking outside
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) overlay.style.display = 'none';
    });
  });
});
