document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('todoModal');
  const taskInput = document.getElementById('newTaskInput');
  const modalList = document.querySelector('.modal-todo-list');
  const widgetList = document.querySelector('.todo-list');
  const addBtn = document.getElementById('addTodoBtn');

  // ✅ モーダル起動
  document.querySelectorAll('[data-modal-target]').forEach(widget => {
    widget.addEventListener('click', () => {
      const modalId = widget.getAttribute('data-modal-target');
      const modalEl = document.getElementById(modalId);
      if (modalEl) modalEl.style.display = 'flex';
    });
  });

  // ✅ モーダル外クリックで閉じる
  document.addEventListener('click', (e) => {
    if (modal && e.target === modal) {
      modal.style.display = 'none';
    }
  });

  // ✅ タスク保存関数
  function saveTasksToLocalStorage(tasks) {
    localStorage.setItem('todo_tasks', JSON.stringify(tasks));
  }

  function loadTasksFromLocalStorage() {
    const saved = localStorage.getItem('todo_tasks');
    return saved ? JSON.parse(saved) : [];
  }

  let tasks = loadTasksFromLocalStorage();

  function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasksToLocalStorage(tasks);
    renderTasks();
  }

  function renderTasks() {
    modalList.innerHTML = '';
    widgetList.innerHTML = '';
    tasks.forEach((task, i) => {
      const modalItem = document.createElement('li');
      modalItem.textContent = task;
      const delBtn = document.createElement('button');
      delBtn.textContent = '🗑️';
      delBtn.style.marginLeft = '8px';
      delBtn.onclick = () => deleteTask(i);
      modalItem.appendChild(delBtn);
      modalList.appendChild(modalItem);

      const widgetItem = document.createElement('li');
      const span = document.createElement('span');
      span.className = 'check-circle';
      span.textContent = '○';
      const shortText = task.length > 6 ? task.slice(0, 6) + '…' : task;
      widgetItem.appendChild(span);
      widgetItem.appendChild(document.createTextNode(' ' + shortText));
      widgetList.appendChild(widgetItem);
    });
  }

  renderTasks();

  if (addBtn && taskInput) {
    addBtn.addEventListener('click', () => {
      const task = taskInput.value.trim();
      if (task === '') return;
      tasks.push(task);
      saveTasksToLocalStorage(tasks);
      renderTasks();
      taskInput.value = '';
    });
  }

  // ✅ メニュー開閉
  document.querySelectorAll('.edit-widget-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const menu = btn.nextElementSibling;
      menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    });
  });

  document.addEventListener('click', () => {
    document.querySelectorAll('.widget-menu').forEach(menu => {
      menu.style.display = 'none';
    });
  });

  document.querySelectorAll('.delete-widget').forEach(delBtn => {
    delBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const widget = delBtn.closest('.widget-box');
      widget.remove();
    });
  });
});
