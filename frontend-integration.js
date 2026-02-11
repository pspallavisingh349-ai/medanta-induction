 API Configuration
const API_URL = httplocalhost8000;

 Utility function for API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method method,
        headers {
            'Content-Type' 'applicationjson',
        },
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail  'Something went wrong');
        }
        
        return result;
    } catch (error) {
        console.error('API Error', error);
        alert('Error ' + error.message);
        throw error;
    }
}

 ==================== PARTICIPANT FUNCTIONS ====================

async function registerParticipant(name, email, department, role, employeeId) {
    const data = {
        name name,
        email email,
        department department,
        role role,
        employee_id employeeId
    };
    const result = await apiCall('apiregister', 'POST', data);
    if (result.success) {
        localStorage.setItem('participantId', result.data.id);
        localStorage.setItem('participantName', result.data.name);
    }
    return result;
}

async function getParticipant(participantId) {
    return await apiCall(`apiparticipant${participantId}`);
}

async function getParticipantByEmail(email) {
    return await apiCall(`apiparticipantemail${email}`);
}

 ==================== ASSESSMENT FUNCTIONS ====================

async function getQuestions() {
    return await apiCall('apiquestions');
}

async function startAssessment(userId) {
    const data = {
        user_id parseInt(userId),
        title Induction Assessment
    };
    return await apiCall('apiassessmentsstart', 'POST', data);
}

async function submitAssessment(answers, timeTaken) {
    const userId = localStorage.getItem('participantId');
    const data = {
        user_id parseInt(userId),
        answers answers,
        time_taken timeTaken
    };
    return await apiCall('apiassessmentssubmit', 'POST', data);
}

async function getAssessmentResult(userId) {
    return await apiCall(`apiresult${userId}`);
}

 ==================== ADMIN FUNCTIONS ====================

async function getDashboardStats() {
    return await apiCall('apiadminstats');
}

async function getAllParticipants() {
    return await apiCall('apiparticipants');
}

async function getAllAssessments() {
    return await apiCall('apiadminassessments');
}

async function addQuestion(question, options, correctAnswer, category = General, marks = 1) {
    const data = {
        question question,
        options options,
        correct_answer correctAnswer,
        category category,
        marks marks
    };
    return await apiCall('apiadminquestions', 'POST', data);
}

 ==================== UTILITY FUNCTIONS ====================

function saveParticipantId(id) {
    localStorage.setItem('participantId', id);
}

function getSavedParticipantId() {
    return localStorage.getItem('participantId');
}

function isRegistered() {
    return !!getSavedParticipantId();
}

function clearParticipant() {
    localStorage.removeItem('participantId');
    localStorage.removeItem('participantName');
}

function logout() {
    clearParticipant();
    window.location.href = 'medanta-dashboard.html';
}