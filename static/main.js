document.addEventListener("DOMContentLoaded", function() {
    fetch("/static/data.json")
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => item.Date);
            const prices = data.map(item => {
                // Virgülü noktaya dönüştürerek fiyatı sayıya çevirin
                const priceStr = item.Price.replace('₺', '').replace('.', '').replace(',', '.').trim();
                return parseFloat(priceStr);
            });

            const ctx = document.getElementById('priceChart').getContext('2d');
            const priceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Product Price (₺)',
                        data: prices,
                        borderColor: 'rgba(75, 192, 192, 2)',
                        borderWidth: 2
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading the data:', error));
});
