// Authentication Form Validation Script


document.addEventListener('DOMContentLoaded', function() {
    // Handle signup form if it exists
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        setupSignupValidation();
    }

    // Handle login form if it exists
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        setupLoginValidation();
    }
});


// SIGNUP FORM VALIDATION

function setupSignupValidation() {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const signupForm = document.getElementById('signup-form');

    // Real-time password strength checker
    if (passwordInput) {
        passwordInput.addEventListener('input', updatePasswordStrength);
    }

    // Real-time password confirmation matcher
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', checkPasswordMatch);
    }

    // Form submission validation
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            if (!validateSignupForm()) {
                e.preventDefault();
            }
        });
    }
}

function updatePasswordStrength() {
    const password = document.getElementById('password').value;
    const strengthMeterFill = document.getElementById('strength-meter-fill');
    const strengthText = document.getElementById('strength-text');

    let strength = 0;
    let strengthLevel = 'Weak';
    let strengthColor = '#dc3545'; // Red

    // Check password length
    if (password.length >= 8) strength += 1;
    if (password.length >= 12) strength += 1;

    // Check for uppercase letters
    if (/[A-Z]/.test(password)) strength += 1;

    // Check for lowercase letters
    if (/[a-z]/.test(password)) strength += 1;

    // Check for numbers
    if (/\d/.test(password)) strength += 1;

    // Check for special characters
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength += 1;

    // Determine strength level
    if (strength <= 2) {
        strengthLevel = 'Weak';
        strengthColor = '#dc3545'; // Red
    } else if (strength <= 4) {
        strengthLevel = 'Fair';
        strengthColor = '#ffc107'; // Yellow
    } else {
        strengthLevel = 'Strong';
        strengthColor = '#28a745'; // Green
    }

    if (password === '') {
        strengthMeterFill.style.height = '0px';
        strengthColor = '#000000';
    }

    if (strength > 0) {
        strengthMeterFill.style.height = '10px';
    }

    // Update visual indicator
    const percentage = (strength / 5) * 100;
    strengthMeterFill.style.width = percentage + '%';
    strengthMeterFill.style.backgroundColor = strengthColor;
    strengthText.textContent = `Password strength: ${strengthLevel}`;
    strengthText.style.color = strengthColor;
}

function checkPasswordMatch() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const matchText = document.getElementById('match-text');

    if (confirmPassword === '') {
        matchText.textContent = '';
        matchText.style.color = '';
        return;
    }

    if (password === confirmPassword) {
        matchText.textContent = '✓ Passwords match';
        matchText.style.color = '#28a745'; // Green
    } else {
        matchText.textContent = '✗ Passwords do not match';
        matchText.style.color = '#dc3545'; // Red
    }
}

function validateSignupForm() {
    const email = document.getElementById('email').value.trim();
    const username = document.getElementById('username').value.trim();
    const firstName = document.getElementById('first_name').value.trim();
    const lastName = document.getElementById('last_name').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    // Check if all fields are filled
    if (!email || !username || !firstName || !lastName || !password || !confirmPassword) {
        showAlert('All fields are required.');
        return false;
    }

    // Validate email format
    if (!isValidEmail(email)) {
        showAlert('Please enter a valid email address.');
        return false;
    }

    // Check if username has appropriate length
    if (username.length < 3) {
        showAlert('Username must be at least 3 characters long.');
        return false;
    }

    // Check minimum password length
    if (password.length < 8) {
        showAlert('Password must be at least 8 characters long.');
        return false;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        showAlert('Passwords do not match.');
        return false;
    }

    // All validations passed
    return true;
}


// LOGIN FORM VALIDATION

function setupLoginValidation() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            if (!validateLoginForm()) {
                e.preventDefault();
            }
        });
    }
}

function validateLoginForm() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    // Check if fields are filled
    if (!email || !password) {
        showAlert('Email and password are required.');
        return false;
    }

    // Validate email format
    if (!isValidEmail(email)) {
        showAlert('Please enter a valid email address.');
        return false;
    }

    // All validations passed
    return true;
}


// UTILITY FUNCTIONS

function isValidEmail(email) {
    // Basic email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(message) {
    alert(message);
}
