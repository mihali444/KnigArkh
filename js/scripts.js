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