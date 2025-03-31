// Главная страница

// function toggleFavorite(button) {
//     button.classList.toggle('active');
// }
// function toggleFavorite(element) {
//     const bookId = element.getAttribute('data-book-id');
//     const heartIcon = element.querySelector('.fa-heart');
//     const csrfToken = "{{ csrf_token }}";
//
//     fetch("{% url 'profile:toggle-favorite' %}", {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//             'X-CSRFToken': csrfToken
//         },
//         body: 'book_id=' + bookId
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 'success') {
//             element.classList.toggle('active', data.is_favorite);
//             heartIcon.classList.toggle('far', !data.is_favorite);
//             heartIcon.classList.toggle('fas', data.is_favorite);
//         } else {
//             alert(data.message || 'Произошла ошибка');
//         }
//     })
//     .catch(error => {
//         console.error('Ошибка:', error);
//         alert('Не удалось выполнить запрос');
//     });
// }

// Страница с объявлением
// document.querySelector('.advertisement-book__favorite-button').addEventListener('click', function () {
//     this.classList.toggle('active');
//     const starIcon = this.querySelector('.star-icon');
//     if (this.classList.contains('active')) {
//         starIcon.classList.replace('far', 'fas'); // Заменяем far на fas
//     } else {
//         starIcon.classList.replace('fas', 'far'); // Заменяем fas на far
//     }
// });

// document.querySelector('.advertisement-book__favorite-button').addEventListener('click', function () {
//     const button = this;
//     const offerId = button.getAttribute('data-offer-id');
//     const starIcon = button.querySelector('.star-icon');
//     const csrfToken = "{{ csrf_token }}";
//
//     fetch("{% url 'profile:toggle-favorite' %}", {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//             'X-CSRFToken': csrfToken
//         },
//         body: 'offer_id=' + offerId
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 'success') {
//             button.classList.toggle('active', data.is_favorite);
//             starIcon.classList.toggle('far', !data.is_favorite);
//             starIcon.classList.toggle('fas', data.is_favorite);
//         } else {
//             alert(data.message || 'Произошла ошибка');
//         }
//     })
//     .catch(error => {
//         console.error('Ошибка:', error);
//         alert('Не удалось выполнить запрос');
//     });
// });

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

