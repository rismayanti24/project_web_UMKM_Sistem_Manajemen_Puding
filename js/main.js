// js/main.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Navbar Scroll Effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 2. Ham Menu Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            const icon = navToggle.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // 3. Update Cart Badge
    updateCartBadge();

    // 4. Modal utilities
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.add('active');
    };

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.remove('active');
    };

    // 5. Cleanup stale dummy orders (orders without tanggal from old seed data)
    const existingOrders = JSON.parse(localStorage.getItem('wp_orders')) || [];
    if (existingOrders.length > 0) {
        const cleanOrders = existingOrders.filter(o => o.tanggal); // Keep only real orders
        if (cleanOrders.length !== existingOrders.length) {
            localStorage.setItem('wp_orders', JSON.stringify(cleanOrders));
        }
    }

    // 6. Scroll Reveal Observer
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target); // Reveal only once
                }
            });
        }, { threshold: 0.15 });
        revealElements.forEach(el => observer.observe(el));
    }

    // 7. Dynamic Featured Products Carousel
    const track = document.getElementById('carouselTrack');
    if (track && typeof getProducts === 'function') {
        const products = getProducts();
        const featuredIds = ['p1', 'p2', 'p7', 'p8'];
        const featuredProducts = featuredIds.map(id => products.find(p => p.id === id)).filter(Boolean);
        
        let htmlContent = '';
        const doubleFeatured = [...featuredProducts, ...featuredProducts];
        
        doubleFeatured.forEach(p => {
            const available = p.stok > 0;
            htmlContent += `
                <div class="carousel-card">
                    <div class="card product-card">
                        <div class="product-image-container">
                            <img src="${p.gambar}" alt="${p.nama}" class="product-image" onerror="this.src='https://placehold.co/300x200/E6CCFF/9B59B6?text=Puding'">
                            ${!available ? '<div class="unavailable-overlay"><span>Habis</span></div>' : ''}
                        </div>
                        <div class="product-info">
                            <h3 class="product-title">${p.nama}</h3>
                            <p class="product-price">${formatRupiah(p.harga)}</p>
                            <a href="detail.html?id=${p.id}" class="btn btn-secondary mt-auto" style="font-size: 0.85rem;">Lihat Detail</a>
                        </div>
                    </div>
                </div>
            `;
        });
        track.innerHTML = htmlContent;
    }
});

function updateCartBadge() {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        const cart = JSON.parse(localStorage.getItem('wp_cart')) || [];
        const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
        badge.textContent = totalItems;
        badge.style.display = totalItems > 0 ? 'flex' : 'none';
    }
}

// Utility: Format Rupiah
function formatRupiah(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

// Utility: Generate Random ID
function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

// Utility: Show Toast
function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    
    toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Utility: Copy to Clipboard
function copyToClipboard(text, successMessage = 'Teks berhasil disalin!') {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(successMessage);
        }).catch(err => {
            console.error('Gagal menyalin teks: ', err);
            showToast('Gagal menyalin teks!', 'error');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";  // Avoid scrolling to bottom
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showToast(successMessage);
        } catch (err) {
            console.error('Fallback: Gagal menyalin teks: ', err);
            showToast('Gagal menyalin teks!', 'error');
        }
        document.body.removeChild(textArea);
    }
}

// Utility: Zoom QRIS Code
function openQrisZoom(imgUrl) {
    let zoomOverlay = document.getElementById('qrisZoomOverlay');
    if (!zoomOverlay) {
        zoomOverlay = document.createElement('div');
        zoomOverlay.id = 'qrisZoomOverlay';
        zoomOverlay.style.position = 'fixed';
        zoomOverlay.style.top = '0';
        zoomOverlay.style.left = '0';
        zoomOverlay.style.width = '100%';
        zoomOverlay.style.height = '100%';
        zoomOverlay.style.backgroundColor = 'rgba(10, 10, 20, 0.85)';
        zoomOverlay.style.backdropFilter = 'blur(8px)';
        zoomOverlay.style.webkitBackdropFilter = 'blur(8px)';
        zoomOverlay.style.zIndex = '100000';
        zoomOverlay.style.display = 'flex';
        zoomOverlay.style.justifyContent = 'center';
        zoomOverlay.style.alignItems = 'center';
        zoomOverlay.style.cursor = 'zoom-out';
        zoomOverlay.style.opacity = '0';
        zoomOverlay.style.transition = 'opacity 0.25s ease';
        
        zoomOverlay.innerHTML = `
            <div style="position: relative; max-width: 90%; max-height: 90%; text-align: center;">
                <img id="qrisZoomImage" src="" style="max-width: 100%; max-height: 80vh; object-fit: contain; border: 3px solid #000; border-radius: 16px; box-shadow: 8px 8px 0 #000; background: white; padding: 15px;">
                <p style="color: white; margin-top: 15px; font-weight: bold; font-family: sans-serif; text-shadow: 1px 1px 2px black; font-size: 0.9rem;">Klik di mana saja untuk menutup</p>
            </div>
        `;
        
        zoomOverlay.addEventListener('click', () => {
            zoomOverlay.style.opacity = '0';
            setTimeout(() => {
                zoomOverlay.style.display = 'none';
            }, 250);
        });
        
        document.body.appendChild(zoomOverlay);
    }
    
    document.getElementById('qrisZoomImage').src = imgUrl;
    zoomOverlay.style.display = 'flex';
    zoomOverlay.offsetHeight; // force reflow
    zoomOverlay.style.opacity = '1';
}


