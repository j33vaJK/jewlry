function applyFilters() {
        const karatageFilters = document.querySelectorAll('input[name="karatage"]:checked');
        const metalFilters = document.querySelectorAll('input[name="metal"]:checked');
        const sortValue = document.querySelector('input[name="sort"]:checked').value;

        const products = document.querySelectorAll('.product');

        products.forEach(product => {
            const productKaratage = product.getAttribute('data-karatage');
            const productMetal = product.getAttribute('data-metal');
            const isVisible = product.style.display !== 'none';

            let showProduct = true;

            // Check if the product matches selected filters
            if (karatageFilters.length > 0) {
                let matchKaratage = false;
                karatageFilters.forEach(filter => {
                    if (productKaratage === filter.value) {
                        matchKaratage = true;
                    }
                });
                if (!matchKaratage) {
                    showProduct = false;
                }
            }

            if (metalFilters.length > 0) {
                let matchMetal = false;
                metalFilters.forEach(filter => {
                    if (productMetal === filter.value) {
                        matchMetal = true;
                    }
                });
                if (!matchMetal) {
                    showProduct = false;
                }
            }

            // Show or hide the product based on filters
            if (showProduct) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });

        // Implement sorting based on sortValue (price_asc or price_desc)
        if (sortValue === 'price_asc') {
            // Sort products by price ascending
            const sortedProducts = Array.from(products).sort((a, b) => {
                const priceA = parseFloat(a.getAttribute('data-price'));
                const priceB = parseFloat(b.getAttribute('data-price'));
                return priceA - priceB;
            });
            document.getElementById('products-container').innerHTML = '';
            sortedProducts.forEach(product => {
                document.getElementById('products-container').appendChild(product);
            });
        } else if (sortValue === 'price_desc') {
            // Sort products by price descending
            const sortedProducts = Array.from(products).sort((a, b) => {
                const priceA = parseFloat(a.getAttribute('data-price'));
                const priceB = parseFloat(b.getAttribute('data-price'));
                return priceB - priceA;
            });
            document.getElementById('products-container').innerHTML = '';
            sortedProducts.forEach(product => {
                document.getElementById('products-container').appendChild(product);
            });
        }
    }