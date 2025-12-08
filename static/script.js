// Simple client-side interactions for filters, auth modal, and sell modal.

// Filters: brand (contains), price min/max
function applyClientFilters() {
    const brandVal = (document.getElementById('brandFilter')?.value || '').toLowerCase().trim();
    const cityVal = (document.getElementById('cityFilter')?.value || '').toLowerCase().trim();
    const currencyVal = (document.getElementById('currencyFilter')?.value || '').trim();
    const minVal = parseFloat(document.getElementById('priceMin')?.value || '0') || 0;
    const maxVal = parseFloat(document.getElementById('priceMax')?.value || '999999999') || 999999999;
    const cards = document.querySelectorAll('#carGrid .card');
    cards.forEach(card => {
        const brand = card.dataset.brand || '';
        const city = card.dataset.city || '';
        const currency = card.dataset.currency || '';
        const price = parseFloat(card.dataset.price || '0') || 0;
        const matchesBrand = !brandVal || brand.includes(brandVal);
        const matchesCity = !cityVal || city.includes(cityVal);
        const matchesCurrency = !currencyVal || currency === currencyVal;
        const matchesPrice = price >= minVal && price <= maxVal;
        card.style.display = matchesBrand && matchesCity && matchesCurrency && matchesPrice ? '' : 'none';
    });
}

function resetFilters() {
    if (document.getElementById('brandFilter')) document.getElementById('brandFilter').value = '';
    if (document.getElementById('priceMin')) document.getElementById('priceMin').value = '';
    if (document.getElementById('priceMax')) document.getElementById('priceMax').value = '';
    applyClientFilters();
}

// Modal helpers
function openModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.add('show');
}
function closeModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.remove('show');
}

// Image preview for sell form
function handleImagePreview(evt) {
    const files = evt.target.files || [];
    const preview = document.getElementById('imagePreview');
    if (!preview) return;
    preview.innerHTML = '';
    Array.from(files).forEach(file => {
        const url = URL.createObjectURL(file);
        const img = document.createElement('img');
        img.src = url;
        img.className = 'thumb';
        preview.appendChild(img);
    });
}

// Wire up events on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    const applyBtn = document.getElementById('applyFilters');
    const resetBtn = document.getElementById('resetFilters');
    applyBtn?.addEventListener('click', (e) => { e.preventDefault(); applyClientFilters(); });
    resetBtn?.addEventListener('click', (e) => { e.preventDefault(); resetFilters(); });

    document.getElementById('sellBtn')?.addEventListener('click', (e) => { e.preventDefault(); openModal('sellModal'); });
    document.getElementById('loginBtn')?.addEventListener('click', (e) => { e.preventDefault(); openModal('authModal'); setAuthMode('login'); });
    document.getElementById('registerBtn')?.addEventListener('click', (e) => { e.preventDefault(); openModal('authModal'); setAuthMode('register'); });

    document.querySelectorAll('.modal .close').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.dataset.close));
    });

    const imageInput = document.getElementById('imageInput');
    imageInput?.addEventListener('change', handleImagePreview);

    document.getElementById('sellForm')?.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Demo: form submission will be wired to backend later.');
        closeModal('sellModal');
    });

    document.getElementById('authForm')?.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Demo: auth will be wired to backend later.');
        closeModal('authModal');
    });

    // Detail page thumbnails: swap main image
    const mainImg = document.getElementById('mainImage');
    const thumbs = document.querySelectorAll('.thumbs img');
    if (mainImg && thumbs.length) {
        thumbs.forEach(t => {
            t.addEventListener('click', () => {
                const src = t.dataset.src || t.src;
                mainImg.src = src;
            });
        });
    }
});

function setAuthMode(mode) {
    const title = document.getElementById('authTitle');
    const submit = document.getElementById('authSubmit');
    if (!title || !submit) return;
    if (mode === 'register') {
        title.textContent = 'Register';
        submit.textContent = 'Register (demo)';
    } else {
        title.textContent = 'Login';
        submit.textContent = 'Login (demo)';
    }
}
