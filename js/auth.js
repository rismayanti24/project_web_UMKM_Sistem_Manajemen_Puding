// js/auth.js
// Firebase Authentication System untuk WarungPudding

// Migrasi: Hapus session lama dari localStorage & sessionStorage (versi sebelumnya)
if (localStorage.getItem('wp_user')) localStorage.removeItem('wp_user');
if (sessionStorage.getItem('wp_user')) sessionStorage.removeItem('wp_user');

// Data user default — akan di-seed ke Firebase Realtime Database jika belum ada
const defaultStaffUsers = [
    { email: 'admin@warungpudding.com', password: 'admin123', role: 'admin', nama: 'Administrator' },
    { email: 'karyawan@warungpudding.com', password: 'karya123', role: 'karyawan', nama: 'Karyawan Stand' }
];

// Helper: get path prefix based on current location
function getPathPrefix() {
    const path = window.location.pathname;
    if (path.includes('/admin/') || path.includes('/karyawan/') || 
        path.includes('\\admin\\') || path.includes('\\karyawan\\')) {
        return '../';
    }
    return '';
}

/**
 * Login menggunakan Firebase Authentication
 * Jika user belum ada di Firebase Auth, otomatis buat akun baru (auto-register)
 * @param {string} username - Username (akan dikonversi ke email)
 * @param {string} password - Password
 * @returns {Promise<boolean>} true jika berhasil login
 */
async function login(username, password) {
    // Konversi username ke format email untuk Firebase Auth
    const email = username.includes('@') ? username : `${username}@warungpudding.com`;
    
    try {
        // Coba login dengan email dan password
        const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
        
        // Pastikan data profil user ada di Realtime Database
        const uid = userCredential.user.uid;
        const snapshot = await db.ref('staff_users/' + uid).once('value');
        
        if (!snapshot.exists()) {
            // Cari data default berdasarkan email
            const defaultUser = defaultStaffUsers.find(u => u.email === email);
            if (defaultUser) {
                await db.ref('staff_users/' + uid).set({
                    email: email,
                    role: defaultUser.role,
                    nama: defaultUser.nama
                });
            }
        }
        
        return true;
    } catch (error) {
        // Jika user belum terdaftar di Firebase Auth, buat akun baru
        if (error.code === 'auth/user-not-found' || error.code === 'auth/invalid-credential') {
            // Cek apakah credential cocok dengan data default
            const defaultUser = defaultStaffUsers.find(u => u.email === email && u.password === password);
            
            if (defaultUser) {
                try {
                    // Buat akun baru di Firebase Auth
                    const newCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
                    
                    // Simpan profil user ke Realtime Database
                    await db.ref('staff_users/' + newCredential.user.uid).set({
                        email: email,
                        role: defaultUser.role,
                        nama: defaultUser.nama
                    });
                    
                    return true;
                } catch (createError) {
                    console.error('Gagal membuat akun:', createError);
                    return false;
                }
            }
        }
        
        console.error('Login gagal:', error.message);
        return false;
    }
}

/**
 * Check Authentication menggunakan Firebase Auth state
 * Mengembalikan Promise yang resolve dengan user data atau null
 * @param {string|null} requiredRole - Role yang diperlukan (admin/karyawan/null)
 * @returns {Promise<object|null>} User data jika valid, null jika tidak
 */
function checkAuth(requiredRole = null) {
    return new Promise((resolve) => {
        // onAuthStateChanged dipanggil sekali saat listener pertama kali di-attach
        const unsubscribe = firebase.auth().onAuthStateChanged(async (firebaseUser) => {
            // Berhenti mendengarkan setelah pengecekan pertama
            unsubscribe();
            
            if (!firebaseUser) {
                // Tidak login — redirect ke login jika role diperlukan
                if (requiredRole) {
                    const prefix = getPathPrefix();
                    window.location.href = prefix + 'login.html';
                }
                resolve(null);
                return;
            }
            
            try {
                // Ambil data profil user dari Realtime Database
                const snapshot = await db.ref('staff_users/' + firebaseUser.uid).once('value');
                const userData = snapshot.val();
                
                if (!userData) {
                    // User ada di Firebase Auth tapi tidak punya profil
                    if (requiredRole) {
                        await firebase.auth().signOut();
                        const prefix = getPathPrefix();
                        window.location.href = prefix + 'login.html';
                    }
                    resolve(null);
                    return;
                }
                
                const user = {
                    uid: firebaseUser.uid,
                    email: firebaseUser.email,
                    role: userData.role,
                    nama: userData.nama
                };
                
                // Cek role jika diperlukan
                if (requiredRole && user.role !== requiredRole) {
                    redirectBasedOnRole(user.role);
                    resolve(null);
                    return;
                }
                
                resolve(user);
            } catch (error) {
                console.error('Error mengambil data user:', error);
                if (requiredRole) {
                    const prefix = getPathPrefix();
                    window.location.href = prefix + 'login.html';
                }
                resolve(null);
            }
        });
    });
}

/**
 * Cek apakah user sedang login (versi cepat, non-blocking)
 * Digunakan untuk halaman publik yang tidak perlu redirect
 * @returns {Promise<object|null>}
 */
function getCurrentUser() {
    return checkAuth(null);
}

// Redirect based on role
function redirectBasedOnRole(role) {
    const prefix = getPathPrefix();

    if (role === 'admin') {
        window.location.href = prefix + 'admin/dashboard.html';
    } else if (role === 'karyawan') {
        window.location.href = prefix + 'karyawan/pesanan.html';
    } else {
        window.location.href = prefix + 'index.html';
    }
}

// Logout menggunakan Firebase Auth
function logout() {
    firebase.auth().signOut().then(() => {
        const prefix = getPathPrefix();
        window.location.href = prefix + 'login.html';
    }).catch((error) => {
        console.error('Logout gagal:', error);
        // Fallback: redirect ke login anyway
        const prefix = getPathPrefix();
        window.location.href = prefix + 'login.html';
    });
}

// Update UI based on auth state (for all pages)
document.addEventListener('DOMContentLoaded', () => {
    firebase.auth().onAuthStateChanged(async (firebaseUser) => {
        const userNameDisplay = document.getElementById('displayUserName');
        
        if (firebaseUser && userNameDisplay) {
            try {
                const snapshot = await db.ref('staff_users/' + firebaseUser.uid).once('value');
                const userData = snapshot.val();
                if (userData) {
                    userNameDisplay.textContent = userData.nama;
                }
            } catch (e) {
                console.error('Gagal update display name:', e);
            }
        }
    });
});
