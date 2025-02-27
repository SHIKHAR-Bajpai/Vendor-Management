/**
 * Authentication utility functions for ShopFinder
 */

// Check authentication status and update UI accordingly
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const loginNav = document.getElementById('loginNav');
    const registerNav = document.getElementById('registerNav');
    const dashboardNav = document.getElementById('dashboardNav');
    const logoutNav = document.getElementById('logoutNav');
    
    if (token) {
        // User is logged in
        if (loginNav) loginNav.classList.add('d-none');
        if (registerNav) registerNav.classList.add('d-none');
        if (dashboardNav) dashboardNav.classList.remove('d-none');
        if (logoutNav) logoutNav.classList.remove('d-none');
        
        // Add logout event listener
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', logout);
        }
    } else {
        // User is not logged in
        if (loginNav) loginNav.classList.remove('d-none');
        if (registerNav) registerNav.classList.remove('d-none');
        if (dashboardNav) dashboardNav.classList.add('d-none');
        if (logoutNav) logoutNav.classList.add('d-none');
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    window.location.href = 'index.html';
}

// Get authentication headers
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Check if token is valid (can be expanded with token validation logic)
function isTokenValid() {
    return !!localStorage.getItem('token');
}

// Redirect if not authenticated
function requireAuth() {
    if (!isTokenValid()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Redirect if already authenticated
function redirectIfAuthenticated(redirectPath = '/dashboard') {
    if (isTokenValid()) {
        window.location.href = redirectPath;
        return true;
    }
    return false;
}