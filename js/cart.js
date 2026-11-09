// js/cart.js

// Default Products (Seed Data)
const defaultProducts = [
    { id: 'p1', nama: 'Puding Coklat Beruang', kategori: 'Coklat', harga: 15000, stok: 20, gambar: 'images/puding dino.jpg', deskripsi: 'Puding rasa coklat lezat dengan bentuk beruang lucu. Cocok untuk pecinta coklat.', tersedia: true },
    { id: 'p2', nama: 'Puding Strawberry Kelinci', kategori: 'Strawberry', harga: 15000, stok: 15, gambar: 'images/kelinci puding.jpeg', deskripsi: 'Puding strawberry segar bentuk kelinci yang sangat menggemaskan.', tersedia: true },
    { id: 'p3', nama: 'Puding Matcha Dino', kategori: 'Matcha', harga: 18000, stok: 10, gambar: 'images/puding dino.jpg', deskripsi: 'Puding rasa matcha otentik dengan bentuk dinosaurus lucu.', tersedia: true },
    { id: 'p4', nama: 'Puding Vanilla Tusuk', kategori: 'Vanilla', harga: 14000, stok: 25, gambar: 'images/puding tusuk.jpg', deskripsi: 'Puding vanilla praktis dengan stik, mudah dinikmati kapan saja.', tersedia: true },
    { id: 'p5', nama: 'Puding Kaki Kucing', kategori: 'Kelinci', harga: 20000, stok: 5, gambar: 'images/kaki kucing puding.jpg', deskripsi: 'Puding berbentuk kaki kucing yang sangat imut.', tersedia: true },
    { id: 'p6', nama: 'Puding Kelinci Pink', kategori: 'Kelinci', harga: 20000, stok: 8, gambar: 'images/kelinci puding.jpeg', deskripsi: 'Puding kelinci pink dengan rasa mix berry.', tersedia: true },
    { id: 'p7', nama: 'Puding Dino Blue', kategori: 'Dinosaurus', harga: 22000, stok: 12, gambar: 'images/dino blue.jpg', deskripsi: 'Puding dinosaurus biru lucu dengan rasa buah blueberry segar.', tersedia: true },
    { id: 'p8', nama: 'Puding Dino Pink', kategori: 'Dinosaurus', harga: 22000, stok: 15, gambar: 'images/dino pink.jpg', deskripsi: 'Puding dinosaurus pink dengan rasa strawberry manis.', tersedia: true },
    { id: 'p9', nama: 'Puding Stik Pelangi', kategori: 'Vanilla', harga: 18000, stok: 15, gambar: 'images/puding tusuk.jpg', deskripsi: 'Puding stik warna warni rasa buah-buahan.', tersedia: true }
];

// Initialize Products in LocalStorage — only seed if not already present
function initProducts() {
    if (!localStorage.getItem('wp_products')) {
        localStorage.setItem('wp_products', JSON.stringify(defaultProducts));
    }
}

// Get Products
function getProducts() {
    initProducts();
    return JSON.parse(localStorage.getItem('wp_products'));
}

// Get Cart
function getCart() {
    return JSON.parse(localStorage.getItem('wp_cart')) || [];
}

// Save Cart
function saveCart(cart) {
    localStorage.setItem('wp_cart', JSON.stringify(cart));
    updateCartBadge();
}

// Check if product is available (stok > 0)
function isProductAvailable(product) {
    return product.stok > 0;
}

// Add to Cart
function addToCart(productId, qty = 1, varian = 'Original') {
    const products = getProducts();
    const product = products.find(p => p.id === productId);
    
    if (!product) return;
    
    if (!isProductAvailable(product)) {
        showToast('Maaf, produk ini sedang tidak tersedia!', 'error');
        return;
    }

    if (product.stok < qty) {
        showToast('Maaf, jumlah yang diminta melebihi ketersediaan!', 'error');
        return;
    }

    const cart = getCart();
    const cartItemId = `${productId}_${varian}`;
    
    const existingItem = cart.find(item => item.cartItemId === cartItemId || (!item.cartItemId && item.id === productId && varian === 'Original'));

    if (existingItem) {
        if (existingItem.qty + qty > product.stok) {
            showToast('Melebihi ketersediaan produk!', 'error');
            return;
        }
        existingItem.qty += qty;
        existingItem.cartItemId = cartItemId;
    } else {
        cart.push({
            cartItemId: cartItemId,
            id: product.id,
            nama: product.nama,
            harga: product.harga,
            gambar: product.gambar,
            qty: qty,
            varian: varian
        });
    }

    saveCart(cart);
    showToast(`${product.nama} (${varian}) ditambahkan ke keranjang!`);
    
    if (typeof renderCart === 'function') {
        renderCart();
    }
}

// Update Quantity
function updateQty(cartItemId, delta) {
    const cart = getCart();
    const products = getProducts();
    const itemIndex = cart.findIndex(item => item.cartItemId === cartItemId || item.id === cartItemId);
    
    if (itemIndex === -1) return;
    
    const item = cart[itemIndex];
    const product = products.find(p => p.id === item.id);
    const newQty = item.qty + delta;
    
    if (newQty <= 0) {
        removeFromCart(cartItemId);
        return;
    }
    
    if (product && newQty > product.stok) {
        showToast('Melebihi ketersediaan produk!', 'error');
        return;
    }
    
    cart[itemIndex].qty = newQty;
    saveCart(cart);
    
    if (typeof renderCart === 'function') {
        renderCart();
    }
}

// Remove from Cart
function removeFromCart(cartItemId) {
    const cart = getCart();
    const updatedCart = cart.filter(item => item.cartItemId !== cartItemId && item.id !== cartItemId);
    saveCart(updatedCart);
    showToast('Item dihapus dari keranjang');
    
    if (typeof renderCart === 'function') {
        renderCart();
    }
}

// Clear Cart
function clearCart() {
    localStorage.removeItem('wp_cart');
    updateCartBadge();
}

// Get Cart Total
function getCartTotal() {
    const cart = getCart();
    return cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initProducts();
});
