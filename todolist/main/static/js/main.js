function addTask() {
    const taskInput = document.getElementById('taskInput');
    const taskList = document.getElementById('taskList');
    const taskValue = taskInput.value.trim();

    if (taskValue === '') return;

    // Remove empty state if present
    const emptyState = taskList.querySelector('.empty');
    if (emptyState) emptyState.remove();

    // Create new task item
    const newTask = document.createElement('li');
    newTask.innerHTML = `
        <span>${taskValue}</span>
        <button class="remove" onclick="removeTask(this)">Remove</button>
    `;
    taskList.appendChild(newTask);

    taskInput.value = '';
}

function removeTask(button) {
    const task = button.parentElement;
    const taskList = task.parentElement;
    task.remove();

    if (taskList.children.length === 0) {
        const emptyMessage = document.createElement('li');
        emptyMessage.className = 'empty';
        emptyMessage.textContent = 'No tasks yet!';
        taskList.appendChild(emptyMessage);
    }
}
