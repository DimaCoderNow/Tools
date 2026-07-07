// Массив товаров
let products = [];

// Отрисовка таблицы
function renderTable() {
    const tbody = document.getElementById('products-tbody');
    tbody.innerHTML = '';

    products.forEach((product, index) => {
        const row = tbody.insertRow();

        // Наименование
        const nameCell = row.insertCell(0);
        const nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.value = product.name;
        nameInput.placeholder = 'Введите товар';
        nameInput.name = `products[${index}][name]`;

        nameInput.addEventListener('input', (e) => {
            products[index].name = e.target.value;
        });

        nameCell.appendChild(nameInput);

        // Количество
        const quantityCell = row.insertCell(1);
        const quantityInput = document.createElement('input');
        quantityInput.type = 'text';
        quantityInput.value = product.quantity;
        quantityInput.placeholder = 'Количество';
        quantityInput.name = `products[${index}][quantity]`;

        quantityInput.addEventListener('input', (e) => {
            products[index].quantity = e.target.value;
        });

        quantityCell.appendChild(quantityInput);

        // Сумма
        const amountCell = row.insertCell(2);
        const amountInput = document.createElement('input');
        amountInput.type = 'number';
        amountInput.value = product.amount;
        amountInput.min = '0';
        amountInput.step = '0.01';
        amountInput.placeholder = 'Сумма';
        amountInput.name = `products[${index}][amount]`;

        amountInput.addEventListener('input', (e) => {
            products[index].amount = e.target.value;
        });

        amountCell.appendChild(amountInput);

        // Удаление строки
        const deleteCell = row.insertCell(3);
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '✖';
        deleteBtn.className = 'delete-row';

        deleteBtn.onclick = () => {
            products.splice(index, 1);
            renderTable();
        };

        deleteCell.appendChild(deleteBtn);
    });
}

// Добавление строки
function addProductRow() {
    products.push({
        name: '',
        quantity: '',
        amount: ''
    });

    renderTable();
}

// Функция для скачивания файла
async function downloadContract() {
    // Собираем данные формы
    const organization = document.getElementById('organization').value;
    const contractNumber = document.getElementById('number').value;
    const contractDate = document.getElementById('date').value;
    const fio = document.getElementById('fio').value;
    const phone = document.getElementById('phone').value;
    const birthDate = document.getElementById('birth_date').value;
    const passportSeries = document.getElementById('passport_series').value;
    const passportNumber = document.getElementById('passport_number').value;
    const passportCode = document.getElementById('passport_code').value;
    const passportDate = document.getElementById('passport_date').value;
    const passportIssued = document.getElementById('passport_issued').value;
    const address = document.getElementById('address').value;
    const total = document.getElementById('contract-total').value || 0;
    const nds = document.getElementById('contract-nds').value || 0;

    // Валидация обязательных полей
    if (!organization) {
        alert('Пожалуйста, выберите организацию');
        return;
    }
    if (!contractNumber) {
        alert('Пожалуйста, введите номер договора');
        return;
    }
    if (!contractDate) {
        alert('Пожалуйста, выберите дату договора');
        return;
    }
    if (!fio) {
        alert('Пожалуйста, введите ФИО покупателя');
        return;
    }
    if (!phone) {
        alert('Пожалуйста, введите телефон');
        return;
    }
    if (!birthDate) {
    alert('Пожалуйста, введите дату рождения');
    return;
    }
    if (!passportSeries) {
        alert('Пожалуйста, введите серию паспорта');
        return;
    }
    if (!passportNumber) {
        alert('Пожалуйста, введите номер паспорта');
        return;
    }
    if (!passportCode) {
        alert('Пожалуйста, введите код подразделения');
        return;
    }
    if (!passportDate) {
        alert('Пожалуйста, введите дату выдачи паспорта');
        return;
    }

    // Создаем FormData для отправки
    const formData = new FormData();
    formData.append('organization', organization);
    formData.append('number', contractNumber);
    formData.append('date', contractDate);
    formData.append('fio', fio);
    formData.append('phone', phone);
    formData.append('birth_date', birthDate);
    formData.append('passport_series', passportSeries);
    formData.append('passport_number', passportNumber);
    formData.append('passport_code', passportCode);
    formData.append('passport_date', passportDate);
    formData.append('passport_issued', passportIssued);
    formData.append('address', address);
    formData.append('total', String(total));
    formData.append('nds', String(nds));
    formData.append('products', JSON.stringify(products));

    // Показываем индикатор загрузки
    const downloadBtn = document.querySelector('[data-target="download"]');
    const originalText = downloadBtn.textContent;
    downloadBtn.textContent = '⏳ Генерация...';
    downloadBtn.style.opacity = '0.7';

    try {
        // Отправляем запрос на сервер
        const response = await fetch('/submit', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            // Получаем файл

            const data = await response.json();

            // Шаг 2: Скачиваем файл через GET-запрос
            const downloadUrl = `/download?file_path=${encodeURIComponent(data.file)}`;
            window.open(downloadUrl, '_blank');

            alert('Договор успешно сгенерирован и скачан!');
        } else {
            const error = await response.json();
            alert(`Ошибка: ${error.detail || 'Не удалось сгенерировать договор'}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке данных на сервер');
    } finally {
        // Восстанавливаем кнопку
        downloadBtn.textContent = originalText;
        downloadBtn.style.opacity = '1';
    }
}

// Активация блоков по клику
const buttons = document.querySelectorAll('.button-full');
const buyerBlock = document.querySelector('.buyer');
const productBlock = document.querySelector('.product');

function removeActiveClassFromButtons() {
    buttons.forEach(btn => {
        btn.classList.remove('active-btn');
    });
}

function hideAllBlocks() {
    buyerBlock.classList.remove('active');
    productBlock.classList.remove('active');
}

buttons.forEach(button => {
    button.addEventListener('click', () => {
        const target = button.getAttribute('data-target');

        hideAllBlocks();
        removeActiveClassFromButtons();

        if (target === 'buyer') {
            buyerBlock.classList.add('active');
            button.classList.add('active-btn');
        } else if (target === 'product') {
            productBlock.classList.add('active');
            button.classList.add('active-btn');
        } else if (target === 'download') {
            downloadContract(); // Вызываем функцию скачивания
        }
    });
});

// Показываем первый блок по умолчанию
buyerBlock.classList.add('active');
buttons[0].classList.add('active-btn');