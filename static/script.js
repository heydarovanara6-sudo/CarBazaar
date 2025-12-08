let favorites = JSON.parse(localStorage.getItem('carbazaar_favorites') || '[]');

function toggleFavorite(id, el) {
    if (favorites.includes(id)) {
        favorites = favorites.filter(f => f !== id);
        el.classList.replace('fa-solid', 'fa-regular');
        el.classList.remove('text-red-600');
    } else {
        favorites.push(id);
        el.classList.replace('fa-regular', 'fa-solid');
        el.classList.add('text-red-600');
    }
    localStorage.setItem('carbazaar_favorites', JSON.stringify(favorites));
}

function applyFilters() {
    const brand = document.getElementById('brands').value;
    const model = document.getElementById('models').value;
    const minPrice = document.getElementById('minPrice').value || 0;
    const maxPrice = document.getElementById('maxPrice').value || 999999;

    fetch(`/api/cars?brand=${brand}&model=${model}&min_price=${minPrice}&max_price=${maxPrice}`)
        .then(r => r.json())
        .then(cars => renderCards(cars));
}

function renderCards(cars) {
    const container = document.getElementById('showCards');
    if (!cars.length) {
        container.innerHTML = '<h1 class="text-4xl text-red-600 col-span-3">No cars found!</h1>';
        return;
    }
    container.innerHTML = cars.map(car => `
        <div class="bg-white rounded-lg shadow hover:shadow-xl transition relative">
            <i onclick="toggleFavorite('${car.id}', this)" class="fa-heart absolute top-4 right-4 text-2xl cursor-pointer z-10 
                ${favorites.includes(car.id) ? 'fa-solid text-red-600' : 'fa-regular'}"></i>
            <a href="/details/${car.id}">
                <img src="${car.images[0]}" class="w-full h-56 object-cover rounded-t-lg" alt="">
            </a>
            <div class="p-4">
                <div class="text-2xl font-bold">${car.price} ${car.currency}</div>
                <div class="text-lg font-semibold uppercase">${car.brand} ${car.model}</div>
                <div class="text-gray-600">${car.year} • ${car.engine}L • ${car.odometer} km</div>
                <div class="text-sm text-gray-500 mt-2">${car.city} • ${car.dates}</div>
            </div>
        </div>
    `).join('');
}
