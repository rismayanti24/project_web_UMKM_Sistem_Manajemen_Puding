// js/validation.js
// Validasi form untuk WarungPudding

/**
 * Validasi input telepon/WhatsApp
 * @param {string} phone - Nomor telepon
 * @returns {boolean} Valid atau tidak
 */
function validatePhone(phone) {
    // Format Indonesia: 08xx, +62xx, 62xx
    const phoneRegex = /^(\+62|62|0)8[1-9][0-9]{7,11}$/;
    return phoneRegex.test(phone.replace(/[\s-]/g, ''));
}

/**
 * Validasi input nama (minimal 3 karakter, hanya huruf dan spasi)
 * @param {string} name - Nama lengkap
 * @returns {boolean} Valid atau tidak
 */
function validateName(name) {
    return name.trim().length >= 3;
}

/**
 * Validasi input alamat (minimal 10 karakter)
 * @param {string} address - Alamat lengkap
 * @returns {boolean} Valid atau tidak
 */
function validateAddress(address) {
    return address.trim().length >= 10;
}

/**
 * Validasi email
 * @param {string} email - Alamat email
 * @returns {boolean} Valid atau tidak
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validasi username (minimal 3 karakter, hanya alfanumerik)
 * @param {string} username - Username
 * @returns {boolean} Valid atau tidak
 */
function validateUsername(username) {
    return username.trim().length >= 3 && /^[a-zA-Z0-9]+$/.test(username);
}

/**
 * Validasi password (minimal 5 karakter)
 * @param {string} password - Password
 * @returns {boolean} Valid atau tidak
 */
function validatePassword(password) {
    return password.length >= 5;
}

/**
 * Tampilkan pesan error pada field tertentu
 * @param {HTMLElement} inputEl - Element input
 * @param {string} message - Pesan error
 */
function showFieldError(inputEl, message) {
    // Hapus error sebelumnya
    clearFieldError(inputEl);
    
    inputEl.style.borderColor = '#E74C3C';
    inputEl.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.15)';
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.cssText = 'color: #E74C3C; font-size: 0.8rem; margin-top: 5px; display: flex; align-items: center; gap: 5px;';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    inputEl.parentElement.appendChild(errorDiv);
}

/**
 * Hapus pesan error pada field tertentu
 * @param {HTMLElement} inputEl - Element input
 */
function clearFieldError(inputEl) {
    inputEl.style.borderColor = '';
    inputEl.style.boxShadow = '';
    
    const existingError = inputEl.parentElement.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Validasi seluruh form checkout
 * @returns {boolean} Apakah form valid
 */
function validateCheckoutForm() {
    let isValid = true;
    
    const nama = document.getElementById('nama');
    const telepon = document.getElementById('telepon');
    const alamat = document.getElementById('alamat');
    
    // Validasi nama
    if (nama && !validateName(nama.value)) {
        showFieldError(nama, 'Nama minimal 3 karakter');
        isValid = false;
    } else if (nama) {
        clearFieldError(nama);
    }
    
    // Validasi telepon
    if (telepon && !validatePhone(telepon.value)) {
        showFieldError(telepon, 'Nomor WhatsApp tidak valid (contoh: 08123456789)');
        isValid = false;
    } else if (telepon) {
        clearFieldError(telepon);
    }
    
    // Validasi alamat
    if (alamat && !validateAddress(alamat.value)) {
        showFieldError(alamat, 'Alamat minimal 10 karakter');
        isValid = false;
    } else if (alamat) {
        clearFieldError(alamat);
    }
    
    return isValid;
}

/**
 * Validasi form login
 * @returns {boolean} Apakah form valid
 */
function validateLoginForm() {
    let isValid = true;
    
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    
    if (username && !validateUsername(username.value)) {
        showFieldError(username, 'Username minimal 3 karakter (alfanumerik)');
        isValid = false;
    } else if (username) {
        clearFieldError(username);
    }
    
    if (password && !validatePassword(password.value)) {
        showFieldError(password, 'Password minimal 5 karakter');
        isValid = false;
    } else if (password) {
        clearFieldError(password);
    }
    
    return isValid;
}

// Auto-clear error saat user mengetik (real-time feedback)
document.addEventListener('DOMContentLoaded', () => {
    // Clear error on input for all form controls
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('input', () => {
            clearFieldError(input);
        });
    });
});
