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