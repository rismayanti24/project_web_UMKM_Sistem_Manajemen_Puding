// js/auth.js

// Data dummy pengguna untuk login simulasi
const dummyUsers = [
    { username: 'admin', password: 'admin123', role: 'admin', nama: 'Administrator' },
    { username: 'karyawan', password: 'karya123', role: 'karyawan', nama: 'Karyawan Stand' },
    { username: 'pelanggan', password: 'user123', role: 'pelanggan', nama: 'Pelanggan Setia' }
];

// Helper: Menentukan awalan jalur (prefix path) berdasarkan lokasi file halaman saat ini
// Ini digunakan agar tautan redirect tetap valid baik saat diakses dari folder akar maupun subfolder (/admin/ atau /karyawan/)
function getPathPrefix() {
    const path = window.location.pathname;
    // Memeriksa jika posisi saat ini berada di dalam subfolder admin atau karyawan
    if (path.includes('/admin/') || path.includes('/karyawan/') || 
        path.includes('\\admin\\') || path.includes('\\karyawan\\')) {
        // Mengembalikan '../' agar naik satu tingkat ke folder akar
        return '../';
    }
    // Mengembalikan string kosong jika sudah berada di folder akar
    return '';
}

// Fungsi utama untuk memeriksa Autentikasi dan Hak Akses Pengguna
function checkAuth(requiredRole = null) {
    // Mengambil data sesi pengguna dari LocalStorage
    const user = JSON.parse(localStorage.getItem('wp_user'));
    
    // Jika data pengguna kosong (belum login) dan halaman tersebut memerlukan peran khusus (requiredRole)
    if (!user && requiredRole) {
        const prefix = getPathPrefix();
        // Alihkan halaman secara otomatis ke halaman login
        window.location.href = prefix + 'login.html';
        return null;
    }
    
    // Jika sudah login, tetapi peran pengguna tidak sesuai dengan peran yang dibutuhkan halaman tersebut
    if (user && requiredRole && user.role !== requiredRole) {
        // Alihkan pengguna ke halaman dashboard yang sesuai dengan peran aslinya
        redirectBasedOnRole(user.role);
        return null;
    }
    
    // Mengembalikan objek user yang valid jika lolos semua pemeriksaan
    return user;
}

// Fungsi untuk mengalihkan halaman otomatis berdasarkan peran (role) pengguna
function redirectBasedOnRole(role) {
    const prefix = getPathPrefix();

    if (role === 'admin') {
        // Jika admin, arahkan ke dashboard admin
        window.location.href = prefix + 'admin/dashboard.html';
    } else if (role === 'karyawan') {
        // Jika karyawan, arahkan ke daftar kelola pesanan karyawan
        window.location.href = prefix + 'karyawan/pesanan.html';
    } else {
        // Jika peran lainnya (atau pelanggan), arahkan ke beranda utama
        window.location.href = prefix + 'index.html';
    }
}

// Fungsi untuk menangani proses Login
function login(username, password) {
    // Mencari kecocokan username dan password pada data dummyUsers
    const user = dummyUsers.find(u => u.username === username && u.password === password);
    
    if (user) {
        // Jika cocok, buat objek sesi (tanpa menyertakan password demi keamanan data)
        const sessionUser = {
            username: user.username,
            role: user.role,
            nama: user.nama
        };
        // Menyimpan data sesi ke LocalStorage browser
        localStorage.setItem('wp_user', JSON.stringify(sessionUser));
        return true; // Mengembalikan true (login berhasil)
    }
    
    return false; // Mengembalikan false jika username/password salah
}

// Fungsi untuk menangani proses Logout
function logout() {
    // Menghapus data sesi 'wp_user' dari LocalStorage
    localStorage.removeItem('wp_user');
    
    const prefix = getPathPrefix();
    // Mengalihkan halaman kembali ke login.html
    window.location.href = prefix + 'login.html';
}

// Mengatur tampilan antarmuka (UI) berdasarkan status autentikasi setelah HTML selesai dimuat
document.addEventListener('DOMContentLoaded', () => {
    // Mengambil data sesi pengguna saat ini
    const user = JSON.parse(localStorage.getItem('wp_user'));
    // Mencari tombol login di navbar
    const loginBtn = document.getElementById('navLoginBtn');
    
    // Jika pengguna sudah login dan tombol login di navbar ditemukan
    if (user && loginBtn) {
        // Ubah teks tombol login menjadi ikon user beserta nama pengguna yang sedang aktif
        loginBtn.innerHTML = '<i class="fas fa-user"></i> ' + user.nama;
        loginBtn.href = '#';
        // Saat nama pengguna di navbar diklik, arahkan ke dashboard yang sesuai perannya
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            redirectBasedOnRole(user.role);
        });
    }
    
    // Untuk halaman dashboard internal, perbarui nama pengguna di sidebar
    const userNameDisplay = document.getElementById('displayUserName');
    if (userNameDisplay && user) {
        userNameDisplay.textContent = user.nama;
    }
});

