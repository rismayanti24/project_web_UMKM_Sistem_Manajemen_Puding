// js/firebase-sync.js

// Inisialisasi awal produk ke Firebase jika database masih kosong
function syncInitialProducts() {
    db.ref('products').once('value', (snapshot) => {
        if (!snapshot.exists()) {
            if (typeof defaultProducts !== 'undefined') {
                db.ref('products').set(defaultProducts);
                console.log("Data produk default berhasil di-upload ke Firebase!");
            }
        } else {
            // Migrasi otomatis jika database berisi produk lama atau harga lama
            const data = snapshot.val();
            if (Array.isArray(data)) {
                const hasOldProduct = data.some(p => p && (p.nama === 'Puding Coklat Beruang' || p.nama === 'Puding Vanilla Tusuk'));
                const hasOldPrices = data.some(p => p && (
                    (p.id === 'p9' && p.harga !== 5000) ||
                    (p.id !== 'p9' && p.harga !== 8000)
                ));
                if ((hasOldProduct || hasOldPrices) && typeof defaultProducts !== 'undefined') {
                    db.ref('products').set(defaultProducts);
                    console.log("Data produk/harga lama terdeteksi! Database berhasil diperbarui.");
                }
            }
        }
    });
}

// Tunggu Firebase terinisialisasi
document.addEventListener('DOMContentLoaded', () => {
    // Jalankan upload awal jika produk kosong
    setTimeout(syncInitialProducts, 1000);
});

// Sinkronisasi data products dari Firebase ke LocalStorage secara Real-time
db.ref('products').on('value', (snapshot) => {
    const data = snapshot.val();
    if (data) {
        localStorage.setItem('wp_products', JSON.stringify(data));
        console.log("Produk lokal disinkronkan dengan Firebase.");
        
        // Kirim event global agar halaman web tahu ada update produk
        window.dispatchEvent(new CustomEvent('wp_products_sync', { detail: data }));
    }
});

// Sinkronisasi data orders dari Firebase ke LocalStorage secara Real-time
db.ref('orders').on('value', (snapshot) => {
    const data = snapshot.val();
    const ordersList = [];
    if (data) {
        // Konversi objek database Firebase ke array pesanan
        Object.keys(data).forEach(key => {
            ordersList.push({ ...data[key], id: key });
        });
    }
    localStorage.setItem('wp_orders', JSON.stringify(ordersList));
    console.log("Pesanan lokal disinkronkan dengan Firebase.");
    
    // Kirim event global agar halaman web tahu ada update pesanan
    window.dispatchEvent(new CustomEvent('wp_orders_sync', { detail: ordersList }));
});
