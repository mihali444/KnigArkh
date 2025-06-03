// Главная страница
// function toggleFavorite(element) {
//     const offerId = element.getAttribute('data-offer-id');
//     const heartIcon = element.querySelector('.fa-heart');
//     const csrfToken = "{{ csrf_token }}";  // CSRF-токен из шаблона
//
//     fetch("{% url 'profile:toggle-favorite' %}", {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//             'X-CSRFToken': csrfToken
//         },
//         body: 'offer_id=' + offerId
//     })
//     .then(response => response.json())  // Всегда ждём JSON
//     .then(data => {
//         if (data.status === 'success') {
//             // Успешное добавление/удаление избранного
//             element.classList.toggle('active', data.is_favorite);
//             heartIcon.classList.toggle('far', !data.is_favorite);  // Пустое сердце
//             heartIcon.classList.toggle('fas', data.is_favorite);   // Заполненное сердце
//         } else if (data.status === 'error' && data.message === 'Требуется вход в систему') {
//             // Перенаправление на страницу входа
//             window.location.href = "{% url 'profile:login' %}?next=" + encodeURIComponent(window.location.pathname);
//         } else {
//             // Другие ошибки (например, "Книга не найдена")
//             alert(data.message || 'Произошла ошибка');
//         }
//     })
//     .catch(error => {
//         console.error('Ошибка:', error);
//         alert('Не удалось выполнить запрос');
//     });
// }

// Страница с объявлением
// document.querySelectorAll('.advertisement-book__favorite-button').forEach(button => {
//     button.addEventListener('click', function () {
//         const offerId = this.getAttribute('data-offer-id');
//         const starIcon = this.querySelector('.star-icon');
//         const csrfToken = "{{ csrf_token }}";
//
//         fetch("/profile/toggle-favorite/", {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//                 'X-CSRFToken': csrfToken
//             },
//             body: 'offer_id=' + offerId
//         })
//         .then(response => response.json()) // Теперь всегда ждём JSON
//         .then(data => {
//             if (data.status === 'success') {
//                 // Успешное добавление/удаление избранного
//                 button.classList.toggle('active', data.is_favorite);
//                 starIcon.classList.toggle('far', !data.is_favorite);
//                 starIcon.classList.toggle('fas', data.is_favorite);
//             } else if (data.status === 'error' && data.message === 'Требуется вход в систему') {
//                 // Перенаправление на страницу входа
//                 window.location.href = "/profile/login/?next=" + encodeURIComponent(window.location.pathname);
//             } else {
//                 // Другие ошибки (например, "Книга не найдена")
//                 alert(data.message || 'Произошла ошибка');
//             }
//         })
//         .catch(error => {
//             console.error('Ошибка:', error);
//             alert('Не удалось выполнить запрос');
//         });
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

