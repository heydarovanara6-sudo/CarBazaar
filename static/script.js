// Simple client-side interactions for filters, auth modal, and sell modal.

// Load More Logic
let visibleCount = 6;
const loadIncrement = 6;

function updateVisibleCars() {
    const cards = document.querySelectorAll('#carFlex .card');
    // Consider currently filtered cards only if we combine with filters, 
    // but for now let's just do simple pagination on the DOM list.
    // Actually, it interacts with filters. 
    // Let's make "Load More" only affect the "limit" of visible items.

    // Better approach for simple client side:
    // Show all matching filters, but only up to 'visibleCount'

    applyClientFilters();
}

// Update applyClientFilters to respect visibleCount? 
// Or separate concerns. Let's separate for simplicity in this hotfix.
// Actually, hiding/showing based on index is easiest.

function initLoadMore() {
    const btn = document.getElementById('loadMoreBtn');
    if (btn) {
        btn.addEventListener('click', () => {
            visibleCount += loadIncrement;
            applyClientFilters(); // Re-run display logic with new count
        });
    }
}

// Refactored applyClientFilters to include Limit
function applyClientFilters() {
    const brandVal = (document.getElementById('brandFilter')?.value || '').toLowerCase().trim();
    const cityVal = (document.getElementById('cityFilter')?.value || '').toLowerCase().trim();
    const currencyVal = (document.getElementById('currencyFilter')?.value || '').trim();
    const minVal = parseFloat(document.getElementById('priceMin')?.value || '0') || 0;
    const maxVal = parseFloat(document.getElementById('priceMax')?.value || '999999999') || 999999999;
    const cards = document.querySelectorAll('#carFlex .card');

    let visibleMatches = 0;
    let totalMatches = 0;

    cards.forEach(card => {
        const brand = card.dataset.brand || '';
        const city = card.dataset.city || '';
        const currency = card.dataset.currency || '';
        const price = parseFloat(card.dataset.price || '0') || 0;
        const matchesBrand = !brandVal || brand.includes(brandVal);
        const matchesCity = !cityVal || city.includes(cityVal);
        const matchesCurrency = !currencyVal || currency === currencyVal;
        const matchesPrice = price >= minVal && price <= maxVal;

        const isMatch = matchesBrand && matchesCity && matchesCurrency && matchesPrice;

        if (isMatch) {
            totalMatches++;
            if (visibleMatches < visibleCount) {
                card.style.display = '';
                visibleMatches++;
            } else {
                card.style.display = 'none';
            }
        } else {
            card.style.display = 'none';
        }
    });

    // Toggle Load More button visibility
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        if (visibleMatches >= totalMatches) {
            loadMoreBtn.style.display = 'none';
        } else {
            loadMoreBtn.style.display = 'inline-block';
        }
    }
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

// Car Data for Dropdowns
const carData = {
    "Acura": ["MDX", "RDX", "TLX", "ILX", "NSX"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale"],
    "Audi": ["A3", "A4", "A5", "A6", "A7", "A8", "Q3", "Q5", "Q7", "Q8", "e-tron", "RS6", "RS7", "R8"],
    "BMW": ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "7 Series", "8 Series", "X1", "X3", "X5", "X6", "X7", "M3", "M4", "M5", "iX", "i4"],
    "Chevrolet": ["Cruze", "Malibu", "Camaro", "Corvette", "Tahoe", "Suburban", "Silverado", "Equinox", "Traverse"],
    "Ford": ["Fiesta", "Focus", "Mustang", "Fusion", "Escape", "Explorer", "Expedition", "F-150", "Ranger", "Bronco"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "HR-V", "Odyssey", "Ridgeline"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Palisade", "Kona", "Venue", "Ioniq"],
    "Infiniti": ["Q50", "Q60", "QX50", "QX60", "QX80"],
    "Kia": ["Rio", "Forte", "K5", "Stinger", "Soul", "Seltos", "Sportage", "Sorento", "Telluride", "Carnival"],
    "Lada (VAZ)": ["Niva", "Priora", "Granta", "Vesta", "2107", "2106", "2101"],
    "Land Rover": ["Range Rover", "Range Rover Sport", "Range Rover Velar", "Evoque", "Discovery", "Defender"],
    "Lexus": ["IS", "ES", "LS", "NX", "RX", "GX", "LX", "LC"],
    "Mazda": ["3", "6", "CX-30", "CX-5", "CX-50", "CX-9", "MX-5 Miata"],
    "Mercedes-Benz": ["A-Class", "C-Class", "E-Class", "S-Class", "GLA", "GLB", "GLC", "GLE", "GLS", "G-Class", "CLA", "CLS", "AMG GT"],
    "Mitsubishi": ["Lancer", "Outlander", "Pajero", "Eclipse Cross", "ASX"],
    "Nissan": ["Sentra", "Altima", "Maxima", "Rogue", "Murano", "Pathfinder", "Patrol", "GT-R", "Z"],
    "Porsche": ["911", "718 Cayman", "718 Boxster", "Panamera", "Macan", "Cayenne", "Taycan"],
    "Toyota": ["Corolla", "Camry", "Avalon", "RAV4", "Highlander", "4Runner", "Land Cruiser", "Prado", "Tacoma", "Tundra", "Prius", "Supra", "Yaris"],
    "Volkswagen": ["Golf", "Jetta", "Passat", "Tiguan", "Atlas", "Touareg", "ID.4"],
    "Volvo": ["S60", "S90", "V60", "V90", "XC40", "XC60", "XC90"]
};

// Wire up events on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    const applyBtn = document.getElementById('applyFilters');
    const resetBtn = document.getElementById('resetFilters');
    applyBtn?.addEventListener('click', (e) => { e.preventDefault(); applyClientFilters(); });
    resetBtn?.addEventListener('click', (e) => { e.preventDefault(); resetFilters(); });

    initLoadMore();
    applyClientFilters(); // Initial run to set visibility


    document.getElementById('sellBtn')?.addEventListener('click', (e) => { e.preventDefault(); openModal('sellModal'); });
    document.getElementById('loginBtn')?.addEventListener('click', (e) => { e.preventDefault(); openModal('authModal'); setAuthMode('login'); });
    document.getElementById('registerBtn')?.addEventListener('click', (e) => { e.preventDefault(); openModal('authModal'); setAuthMode('register'); });

    document.querySelectorAll('.modal .close').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.dataset.close));
    });

    const imageInput = document.getElementById('imageInput');
    imageInput?.addEventListener('change', handleImagePreview);

    // Initialize Brand Dropdown
    const brandSelect = document.getElementById('brandSelect');
    const modelSelect = document.getElementById('modelSelect');

    if (brandSelect && modelSelect) {
        // Populate Brands
        const sortedBrands = Object.keys(carData).sort();
        sortedBrands.forEach(brand => {
            const opt = document.createElement('option');
            opt.value = brand;
            opt.textContent = brand;
            brandSelect.appendChild(opt);
        });

        // Handle Brand Change
        brandSelect.addEventListener('change', () => {
            const brand = brandSelect.value;
            modelSelect.innerHTML = '<option value="" disabled selected>Select Model</option>';

            if (brand && carData[brand]) {
                carData[brand].sort().forEach(model => {
                    const opt = document.createElement('option');
                    opt.value = model;
                    opt.textContent = model;
                    modelSelect.appendChild(opt);
                });
                modelSelect.disabled = false;
            } else {
                modelSelect.disabled = true;
            }
        });
    }

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
