// Получаем элементы
const fileInput = document.getElementById('bookCover');
const uploadArea = document.querySelector('.book-cover-upload');

// Хранилище для файлов
let uploadedFiles = [];

// Добавляем контейнер для отображения выбранных файлов
const uploadedFilesContainer = document.createElement('div');
uploadedFilesContainer.className = 'uploaded-files';
uploadArea.appendChild(uploadedFilesContainer);

// Обработка выбора файлов через кнопку
fileInput.addEventListener('change', handleFiles);

// Обработка перетаскивания
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#F2800D';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#ccc';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#ccc';
    
    // Получаем файлы из события drop
    const files = Array.from(e.dataTransfer.files);
    handleDroppedFiles(files);
});

// Функция для обработки файлов из input
function handleFiles(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

// Функция для обработки файлов из drop
function handleDroppedFiles(files) {
    addFiles(files);
    
    // Обновляем input с новым списком файлов
    updateFileInput();
}

// Добавляем новые файлы в хранилище
function addFiles(newFiles) {
    // Фильтруем только файлы (исключаем папки и т.п.)
    const validFiles = newFiles.filter(file => file.type.startsWith('image/'));
    
    // Добавляем только уникальные файлы
    validFiles.forEach(file => {
        if (!uploadedFiles.some(f => f.name === file.name && f.size === file.size)) {
            uploadedFiles.push(file);
        }
    });
    
    displayFiles();
}

// Обновляем input с новым списком файлов
function updateFileInput() {
    const dataTransfer = new DataTransfer();
    uploadedFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
}

// Функция отображения выбранных файлов
function displayFiles() {
    uploadedFilesContainer.innerHTML = '';
    
    if (uploadedFiles.length === 0) {
        uploadedFilesContainer.innerHTML = '<p class="no-files">Файлы не выбраны</p>';
        return;
    }

    // Создаем список выбранных файлов
    const fileList = document.createElement('ul');
    fileList.className = 'file-list';
    
    uploadedFiles.forEach(file => {
        const li = document.createElement('li');
        li.className = 'file-item';
        li.textContent = `${file.name} (${Math.round(file.size/1024)} KB)`;
        
        // Кнопка удаления
        const removeBtn = document.createElement('button');
        removeBtn.className = 'file-remove';
        removeBtn.textContent = '×';
        removeBtn.onclick = () => {
            uploadedFiles = uploadedFiles.filter(f => f !== file);
            updateFileInput();
            displayFiles();
        };
        
        li.appendChild(removeBtn);
        fileList.appendChild(li);
    });
    
    uploadedFilesContainer.appendChild(fileList);
}

// Инициализация пустого состояния
displayFiles();




// Логика для кастомного селекта
document.querySelector('.custom-select-input').addEventListener('click', function () {
    const dropdown = document.querySelector('.custom-select-dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
  });
  
  document.querySelectorAll('.custom-select-option input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      const selected = Array.from(document.querySelectorAll('.custom-select-option input[type="checkbox"]:checked'))
        .map(cb => cb.value);
      document.getElementById('categoryDisplay').value = selected.join(', ');
    });
  });
  
  // Закрытие выпадающего списка при клике вне его
  document.addEventListener('click', function (event) {
    const select = document.querySelector('.custom-select');
    if (!select.contains(event.target)) {
      document.querySelector('.custom-select-dropdown').style.display = 'none';
    }
  });