// Главная страница

function toggleFavorite(button) {
    button.classList.toggle('active'); 
}


// Страница с объявлением

document.querySelector('.advertisement-book__favorite-button').addEventListener('click', function () {
    this.classList.toggle('active');
    const starIcon = this.querySelector('.star-icon');
    if (this.classList.contains('active')) {
        starIcon.classList.replace('far', 'fas'); // Заменяем far на fas
    } else {
        starIcon.classList.replace('fas', 'far'); // Заменяем fas на far
    }
});

// Страница со входом

function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password i');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.replace('fa-eye-slash', 'fa-eye'); // Показываем глазик
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.replace('fa-eye', 'fa-eye-slash'); // Скрываем глазик
    }
}

function redirectToEmailPage() {
    // Здесь можно добавить проверку данных перед переходом
    const emailInput = document.getElementById('email');

    if (emailInput.value.trim() === '') {
        alert('Пожалуйста, заполните все поля!');
        return;
    }

    // Переход на другую страницу
    window.location.href = './enter-email.html'; // Замените на нужный URL
}

function redirectToPasswordPage() {
    // Здесь можно добавить проверку данных перед переходом
    const codeInput = document.getElementById('code');

    if (codeInput.value.trim() === '') {
        alert('Пожалуйста, заполните все поля!');
        return;
    }

    // Переход на другую страницу
    console.log('Кнопка нажата!');
    window.location.href = './new-password.html'; // Замените на нужный URL
}

function redirectToLoginPage() {
    // Здесь можно добавить проверку данных перед переходом
    const passwordInput = document.getElementById('password');

    if (passwordInput.value.trim() === '') {
        alert('Пожалуйста, заполните все поля!');
        return;
    }

    // Переход на другую страницу
    console.log('Кнопка нажата!');
    window.location.href = './logIn.html'; // Замените на нужный URL
}

document.addEventListener('DOMContentLoaded', function () {
    fetchReviews();
});

function fetchReviews() {
    fetch('/api/reviews')
        .then(response => response.json())
        .then(data => {
            updateRating(data);
            updateChart(data);
        })
        .catch(error => console.error('Ошибка:', error));
}

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


// Получаем все кнопки табов
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const activeAdContainer = document.getElementById('active-ad');
    const completeAdContainer = document.getElementById('complete-ad');

    function switchTabs(event) {
        console.log('Кнопка нажата:', event.target.textContent);

        tabs.forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');

        const selectedTab = event.target.getAttribute('data-tab');

        activeAdContainer.classList.add('hidden-ad');
        completeAdContainer.classList.add('hidden-ad');

        if (selectedTab === 'active') {
            activeAdContainer.classList.remove('hidden-ad');
        } else if (selectedTab === 'completed') {
            completeAdContainer.classList.remove('hidden-ad');
        }
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', switchTabs);
    });
});