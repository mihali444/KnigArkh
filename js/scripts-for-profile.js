const data = {
    reviews: [
        { rating: 5 },
        { rating: 5 },
        { rating: 5 },
        { rating: 4 },
        { rating: 5 },
        { rating: 3 },
        { rating: 5 },
        { rating: 5 },
        { rating: 5 },
        { rating: 4 },
        { rating: 5 },
        { rating: 5 }
    ],
    comments: [
        { text: "Отличная книга!" },
        { text: "Советую всем." },
        { text: "Хороший сюжет." },
        { text: "Понравилось." },
        { text: "Класс!" },
        { text: "Великолепно!" },
        { text: "Читается легко." },
        { text: "Очень интересно." }
    ]
};

document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.tab');
    const activeAd = document.getElementById('active-ad');
    const completeAd = document.getElementById('complete-ad');

    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            // Удаляем класс 'active' со всех вкладок
            tabs.forEach(t => t.classList.remove('active'));

            // Добавляем класс 'active' только к выбранной вкладке
            this.classList.add('active');

            // Проверяем, какая вкладка была выбрана
            if (this.getAttribute('data-tab') === 'active') {
                activeAd.classList.remove('hidden-ad'); // Показываем активные объявления
                completeAd.classList.add('hidden-ad');   // Скрываем завершенные объявления
            } else if (this.getAttribute('data-tab') === 'completed') {
                completeAd.classList.remove('hidden-ad'); // Показываем завершенные объявления
                activeAd.classList.add('hidden-ad');      // Скрываем активные объявления
            }
        });
    });
});

function updateRating(data) {
    const averageRating = calculateAverageRating(data.reviews);
    const totalReviews = data.reviews.length;
    const totalComments = data.comments.length;

    document.querySelector('.average-rating').textContent = averageRating.toFixed(1);
    document.querySelector('.total-reviews').textContent = `${totalReviews} оценок`;
    document.querySelector('.total-comments').textContent = `${totalComments} отзывов`;
}

function updateChart(data) {
    const chartRows = document.querySelectorAll('.chart-row');
    const ratingsCount = countRatings(data.reviews);

    chartRows.forEach(row => {
        const ratingLabel = row.querySelector('.rating-label').textContent;
        const bar = row.querySelector('.bar');
        const countSpan = row.querySelector('.count');

        const count = ratingsCount[ratingLabel] || 0;
        const percentage = count / data.reviews.length * 100;

        bar.style.width = `${percentage}%`;
        countSpan.textContent = count;
    });
}

function calculateAverageRating(reviews) {
    if (reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, review) => acc + review.rating, 0);
    return sum / reviews.length;
}

function countRatings(reviews) {
    const counts = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 };
    reviews.forEach(review => {
        counts[review.rating]++;
    });
    return counts;
}

document.addEventListener('DOMContentLoaded', function () {
    // Обновляем средний рейтинг и количество отзывов
    updateRating(data);

    // Обновляем диаграмму рейтинга
    updateChart(data);
});

document.querySelector('.advertisement-book__favorite-button').addEventListener('click', function () {
    this.classList.toggle('active');
    const starIcon = this.querySelector('.star-icon');
    if (this.classList.contains('active')) {
        starIcon.classList.replace('far', 'fas'); // Заменяем far на fas
    } else {
        starIcon.classList.replace('fas', 'far'); // Заменяем fas на far
    }
});

function redirectToEditingPage() {
    console.log('Кнопка нажата!');
    window.location.href = './profile-edit.html'; 
}

