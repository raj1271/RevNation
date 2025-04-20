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

document.addEventListener("DOMContentLoaded", function() {
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

function filterProducts(category) {
    let products = document.querySelectorAll('.product-card');
    products.forEach(product => {
        if (product.getAttribute('data-category') === category || category === 'all') {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

document.getElementById("sort-options").addEventListener("change", function() {
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