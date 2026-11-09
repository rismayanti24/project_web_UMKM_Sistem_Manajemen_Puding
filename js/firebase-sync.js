// js/firebase-sync.js

// Fungsi untuk mengunggah produk default ke Firebase saat pertama kali dijalankan (jika Firebase masih kosong)
function syncInitialProducts() {
    // Membaca data dari path 'products' di Firebase Realtime Database sekali saja
    db.ref('products').once('value', (snapshot) => {
        // Memeriksa apakah data produk sudah ada di Firebase
        if (!snapshot.exists()) {
            // Memeriksa apakah variabel defaultProducts (dari database produk lokal) sudah didefinisikan
            if (typeof defaultProducts !== 'undefined') {
                // Mengunggah data defaultProducts ke path 'products' di Firebase
                db.ref('products').set(defaultProducts);
                // Menampilkan log sukses ke konsol browser
                console.log("Data produk default berhasil di-upload ke Firebase!");
            }
        }
    });
}

// Menunggu seluruh elemen halaman web selesai dimuat (DOM ready)
document.addEventListener('DOMContentLoaded', () => {
    // Menjalankan fungsi sinkronisasi awal setelah delay 1 detik (1000 milidetik) agar Firebase siap
    setTimeout(syncInitialProducts, 1000);
});

// Mendengarkan perubahan data pada path 'products' di Firebase secara real-time (aktif terus-menerus)
db.ref('products').on('value', (snapshot) => {
    // Mengambil nilai data terbaru dari snapshot Firebase
    const data = snapshot.val();
    // Memastikan data produk tidak kosong/null
    if (data) {
        // Menyimpan data produk terbaru ke LocalStorage browser dalam format JSON String
        localStorage.setItem('wp_products', JSON.stringify(data));
        // Menampilkan log sinkronisasi produk sukses ke konsol
        console.log("Produk lokal disinkronkan dengan Firebase.");
        
        // Memancarkan event kustom 'wp_products_sync' ke seluruh jendela browser
        // agar halaman web yang aktif bisa mendeteksi perubahan produk dan me-render ulang antarmuka
        window.dispatchEvent(new CustomEvent('wp_products_sync', { detail: data }));
    }
});

// Mendengarkan perubahan data pada path 'orders' di Firebase secara real-time (aktif terus-menerus)
db.ref('orders').on('value', (snapshot) => {
    // Mengambil nilai data pesanan dari snapshot Firebase
    const data = snapshot.val();
    // Membuat array kosong untuk menyimpan daftar pesanan yang diformat
    const ordersList = [];
    // Memeriksa apakah ada data pesanan di Firebase
    if (data) {
        // Firebase menyimpan data sebagai objek berpasangan (key-value), kita ubah menjadi array
        // Iterasi melalui setiap kunci (Order ID) dari objek data pesanan
        Object.keys(data).forEach(key => {
            // Memasukkan data pesanan ke array dengan menyertakan kunci unik Firebase sebagai properti 'id'
            ordersList.push({ ...data[key], id: key });
        });
    }
    // Menyimpan daftar pesanan terbaru ke LocalStorage browser dalam format JSON String
    localStorage.setItem('wp_orders', JSON.stringify(ordersList));
    // Menampilkan log sinkronisasi pesanan sukses ke konsol
    console.log("Pesanan lokal disinkronkan dengan Firebase.");
    
    // Memancarkan event kustom 'wp_orders_sync' ke seluruh jendela browser
    // agar halaman web (seperti halaman admin & karyawan) tahu ada pesanan masuk/update dan me-render ulang tabel
    window.dispatchEvent(new CustomEvent('wp_orders_sync', { detail: ordersList }));
});

