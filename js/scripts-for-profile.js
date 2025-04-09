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