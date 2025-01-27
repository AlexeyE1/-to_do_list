document.addEventListener('DOMContentLoaded', function() {
    const completeButtons = document.querySelectorAll('.complete');
    
    completeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Останавливаем стандартное поведение кнопки

            const taskItem = event.target.closest('li');
            const taskList = document.getElementById('taskList');
            const formAction = taskItem.querySelector('form').action;

            // Используем регулярное выражение для извлечения ID из URL
            const taskIdMatch = formAction.match(/(\d+)\/$/);
            const sessionIndexMatch = formAction.match(/session\/(\d+)\/$/);

            let urlPath = '';
            
            // Проверяем, является ли задача задачей из сессии или из базы данных
            if (sessionIndexMatch) {
                urlPath = `/change_status/session/${sessionIndexMatch[1]}/`; // Путь для задач из сессии
            } else if (taskIdMatch) {
                urlPath = `/change_status/${taskIdMatch[1]}/`; // Путь для задач из базы данных
            }

            // Если URL не содержит ID, выходим
            if (!urlPath) return;

            // Добавляем класс для анимации перемещения
            taskItem.classList.add('task-move');

            // Если задача не помечена как выполненная
            if (!taskItem.querySelector('.task_completed')) {
                taskItem.querySelector('span').classList.add('task_completed');
                
                // Плавно перемещаем задачу вниз через другие элементы
                let nextSibling = taskItem.nextElementSibling;
                let distance = 0;

                // Плавно двигаем задачу вниз через другие элементы
                const moveDown = setInterval(function() {
                    if (nextSibling) {
                        taskItem.style.top = `${distance}px`;
                        distance += taskItem.offsetHeight + 5; // Двигаем на высоту задачи + небольшой отступ
                        nextSibling = nextSibling.nextElementSibling;
                    } else {
                        // После завершения анимации перемещаем задачу в конец
                        taskList.appendChild(taskItem);
                        taskItem.style.top = '0px'; // сбрасываем стиль top
                        clearInterval(moveDown);
                    }
                }, 70); // Увеличиваем интервал, чтобы анимация была медленнее

                // Отправляем запрос на сервер для изменения статуса задачи
                fetch(urlPath, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Отправляем csrf токен
                    },
                    body: JSON.stringify({ completed: true })
                })
                .then(response => response.json())
                .then(data => {
                    // Обработка успешного ответа (если нужно)
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });
});