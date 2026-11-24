// ===== DOM Elements =====
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('loginBtn');
const togglePasswordBtn = document.getElementById('togglePassword');

const signupModal = document.getElementById('signupModal');
const signupForm = document.getElementById('signupForm');
const signupEmail = document.getElementById('signupEmail');
const signupFullname = document.getElementById('signupFullname');
const signupUsername = document.getElementById('signupUsername');
const signupPassword = document.getElementById('signupPassword');
const signupBtn = document.getElementById('signupBtn');

const signupLink = document.getElementById('signupLink');
const loginLink = document.getElementById('loginLink');
const backToLogin = document.getElementById('backToLogin');

const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

const successModal = document.getElementById('successModal');
const successTitle = document.getElementById('successTitle');
const successMsg = document.getElementById('successMsg');

// ===== Enable/Disable Login Button =====
function updateLoginBtn() {
    if (usernameInput.value.trim() && passwordInput.value) {
        loginBtn.classList.add('active');
        loginBtn.disabled = false;
    } else {
        loginBtn.classList.remove('active');
        loginBtn.disabled = true;
    }
}
usernameInput.addEventListener('input', updateLoginBtn);
passwordInput.addEventListener('input', updateLoginBtn);

// ===== Enable/Disable Signup Button =====
function updateSignupBtn() {
    if (
        signupEmail.value.trim() &&
        signupFullname.value.trim() &&
        signupUsername.value.trim() &&
        signupPassword.value.length >= 6
    ) {
        signupBtn.classList.add('active');
        signupBtn.disabled = false;
    } else {
        signupBtn.classList.remove('active');
        signupBtn.disabled = true;
    }
}
signupEmail.addEventListener('input', updateSignupBtn);
signupFullname.addEventListener('input', updateSignupBtn);
signupUsername.addEventListener('input', updateSignupBtn);
signupPassword.addEventListener('input', updateSignupBtn);

// ===== Toggle Password =====
togglePasswordBtn.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        togglePasswordBtn.textContent = 'Hide';
    } else {
        passwordInput.type = 'password';
        togglePasswordBtn.textContent = 'Show';
    }
});

// ===== Show Toast =====
function showToast(message, type = 'error') {
    toastMessage.textContent = message;
    toast.className = 'toast show ' + type;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ===== Show Success =====
function showSuccess(title, msg) {
    successTitle.textContent = title;
    successMsg.textContent = msg;
    successModal.classList.add('show');
}

// ===== Login Submit =====
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    loginBtn.textContent = 'Logging in...';
    loginBtn.disabled = true;

    try {
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();

        if (data.success) {
            showSuccess('Login Successful!', data.message);
            loginForm.reset();
            updateLoginBtn();
        } else {
            showToast(data.message, 'error');
        }
    } catch (err) {
        showToast('Something went wrong. Please try again.', 'error');
    }

    loginBtn.textContent = 'Log in';
    loginBtn.disabled = false;
    loginBtn.classList.remove('active');
});

// ===== Signup Submit =====
signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = signupEmail.value.trim();
    const fullname = signupFullname.value.trim();
    const username = signupUsername.value.trim();
    const password = signupPassword.value;

    signupBtn.textContent = 'Signing up...';
    signupBtn.disabled = true;

    try {
        const res = await fetch('/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, fullname, username, password })
        });
        const data = await res.json();

        if (data.success) {
            signupModal.classList.remove('show');
            showSuccess('Account Created!', data.message);
            signupForm.reset();
            updateSignupBtn();
        } else {
            showToast(data.message, 'error');
        }
    } catch (err) {
        showToast('Something went wrong. Please try again.', 'error');
    }

    signupBtn.textContent = 'Sign up';
    signupBtn.disabled = false;
    signupBtn.classList.remove('active');
});

// ===== Modal Toggle =====
signupLink.addEventListener('click', (e) => {
    e.preventDefault();
    signupModal.classList.add('show');
});

loginLink.addEventListener('click', (e) => {
    e.preventDefault();
    signupModal.classList.remove('show');
});

backToLogin.addEventListener('click', () => {
    signupModal.classList.remove('show');
});
