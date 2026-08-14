document.addEventListener('DOMContentLoaded', function() {
    // Handle edit form if it exists
    const usernameForm = document.getElementById('username-form');
    if (usernameForm) {
        setupUsernameValidation();
    }
    const passwordForm = document.getElementById('password-form');
    if (passwordForm) {
        setupPasswordValidation();
    }
});

// Username Validation

function setupUsernameValidation() {
    const usernameForm = document.getElementById('username-form');
    const usernameInput = document.getElementById('username')

    if (usernameForm) {
        usernameForm.addEventListener('submit', function(e) {
            if (!validateUsernameForm()) {
                e.preventDefault();
            }
        });
    }
}

function validateUsernameForm() {
    const username = document.getElementById('username').value.trim();

    if (!username) {
        showAlert('Please enter a new username');
        return false;
    }

    // Check if username has appropriate length
    if (username.length < 3) {
        showAlert('Username must be at least 3 characters long.');
        return false;
    }

    //Check if username fits requirements
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(username) || /\s/.test(username)) {
        showAlert('Username cannot include special Characters or Spaces');
        return false;
    }

    if (username.length > 20) {
        showAlert('Username cannot be longer than 20 characters');
        return false;
    }

    // All validations passed
    return true;
}

function setupPasswordValidation() {
    const passwordForm = document.getElementById('password-form');
    const oldPasswordInput = document.getElementById('current_password');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');

    // Real-time password strength checker
    if (passwordInput) {
        passwordInput.addEventListener('input', updatePasswordStrength);
    }

    // Real-time password confirmation matcher
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', checkPasswordMatch);
    }

    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            if (!validatePasswordForm()) {
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

function validatePasswordForm() {
    const oldPasswordInput = document.getElementById('current_password');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');

    if (!oldPasswordInput || !passwordInput || !confirmPasswordInput) {
        showAlert('All fields are required.');
        return false;
    }

    // Check if password meets requirement
    if (/\s/.test(passwordInput.value)) {
        showAlert('Password cannot include Spaces');
        return false;
    }

    // Check minimum password length
    if (passwordInput.value.length < 8) {
        showAlert('Password must be at least 8 characters long.');
        return false;
    }

    // Check if passwords match
    if (passwordInput.value !== confirmPasswordInput.value) {
        showAlert('Passwords do not match.');
        return false;
    }

    // All validations passes
    return true;
}

function showAlert(message) {
    alert(message);
}

