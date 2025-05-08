document.addEventListener("DOMContentLoaded", function () {
    // Fade-in animation for products on scroll
    const fadeElements = document.querySelectorAll(".fade-in");
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
            }
        });
    }, { threshold: 0.5 });

    fadeElements.forEach(el => observer.observe(el));

    // Button click animation
    document.querySelectorAll(".btn").forEach(button => {
        button.addEventListener("click", function () {
            this.classList.add("clicked");
            setTimeout(() => this.classList.remove("clicked"), 300);
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let items = document.querySelectorAll(".pd-item");
    let observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, { threshold: 0.5 });
    items.forEach(item => observer.observe(item));
});

function checkAnswer(answer) {
    let result = document.getElementById("quiz-result");
    if (answer === "Helmet") {
        result.textContent = "Correct! A helmet is the most essential safety gear.";
    } else {
        result.textContent = "Try again! The helmet is the most important safety gear.";
    }
}


// Shop

document.getElementById('category-dropdown').addEventListener('change', function () {
    const category = this.value;
    filterProducts(category);
});

function filterProducts(category) {
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

document.getElementById("sort-options").addEventListener("change", function () {
    let products = Array.from(document.querySelectorAll(".product-card"));
    let sortType = this.value;

    if (sortType === "price-low") {
        products.sort((a, b) => parseFloat(a.dataset.price) - parseFloat(b.dataset.price));
    } else if (sortType === "price-high") {
        products.sort((a, b) => parseFloat(b.dataset.price) - parseFloat(a.dataset.price));
    } else if (sortType === "name-asc") {
        products.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name));
    } else if (sortType === "name-desc") {
        products.sort((a, b) => b.dataset.name.localeCompare(a.dataset.name));
    }

    let container = document.getElementById("product-list");
    container.innerHTML = ""; // Clear the existing products
    products.forEach(product => container.appendChild(product)); // Append sorted products
});


function search() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const items = document.querySelectorAll('.item');
    const noResults = document.getElementById('noResults');

    let found = false;

    items.forEach(item => {
        const name = item.getAttribute('data-name').toLowerCase();
        if (name.includes(input)) {
            item.style.display = 'block';
            found = true;
        } else {
            item.style.display = 'none';
        }
    });

    // Show "No results found" if nothing matches
    if (!found) {
        noResults.style.display = 'block';
    } else {
        noResults.style.display = 'none';
    }
}