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

document.getElementById('loginForm').addEventListener('submit', function (event) {
    // Предотвращаем отправку формы
    event.preventDefault();

    // Получаем значение поля ввода
    const usernameInput = document.getElementById('username');
    const usernameValue = usernameInput.value.trim();
    const usernameError = document.getElementById('usernameError');

    // Очищаем предыдущие сообщения об ошибках
    usernameError.textContent = '';
    usernameError.classList.remove('visible');

    // Проверяем, является ли ввод корректным email или телефоном
    const isEmailValid = validateEmail(usernameValue);
    const isPhoneValid = validatePhone(usernameValue);

    if (!isEmailValid && !isPhoneValid) {
        // Если данные некорректны, показываем сообщение об ошибке
        usernameError.textContent = 'Введите корректный email или телефон';
        usernameError.classList.add('visible');
    } else {
        // Если данные корректны, отправляем форму
        alert('Форма отправлена успешно!');
        // Здесь можно выполнить отправку данных на сервер
        // this.submit();
    }
});

// Функция для проверки email
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Функция для проверки телефона
function validatePhone(phone) {
    const phoneRegex = /^\+?[0-9]{10,15}$/; // Пример: +79991234567 или 9991234567
    return phoneRegex.test(phone);
}