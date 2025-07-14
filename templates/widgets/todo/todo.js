document.addEventListener('DOMContentLoaded', () => {
  // ToDo入力処理
  document.querySelectorAll('.todo-input').forEach(input => {
    input.addEventListener('keypress', function (e) {
      if (e.key === 'Enter' && this.value.trim() !== '') {
        const li = document.createElement('li');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.addEventListener('change', () => {
          li.style.textDecoration = checkbox.checked ? 'line-through' : 'none';
        });

        li.appendChild(checkbox);
        li.appendChild(document.createTextNode(this.value));
        this.closest('.todo-list').querySelector('.todo-items').appendChild(li);
        this.value = '';
      }
    });
  });

  // ウィジェットメニューの開閉
  document.querySelectorAll('.edit-widget-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const menu = btn.nextElementSibling;
      menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    });
  });

  // 外部クリックでメニュー閉じる
  document.addEventListener('click', () => {
    document.querySelectorAll('.widget-menu').forEach(menu => {
      menu.style.display = 'none';
    });
  });

  // 削除ボタンの挙動
  document.querySelectorAll('.delete-widget').forEach(delBtn => {
    delBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const widget = delBtn.closest('.widget-box');
      widget.remove();
    });
  });
});

function openTodoModal() {
  document.getElementById("todoModal").style.display = "block";
}

document.getElementById("todoInput").addEventListener("keypress", function(e) {
  if (e.key === "Enter" && this.value.trim() !== "") {
    const li = document.createElement("li");
    li.innerText = this.value;
    document.getElementById("todoList").appendChild(li);
    this.value = "";
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("todoModal");

  // ウィジェットクリックでモーダルを表示
  document.querySelectorAll(".todo-widget").forEach(widget => {
    widget.addEventListener("click", function () {
      modal.classList.remove("hidden");
    });
  });

  // モーダル外をクリックしたら閉じる
  modal.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.classList.add("hidden");
    }
  });

  // 追加ボタンの処理（仮保存）
  const addBtn = document.getElementById("addTaskBtn");
  const input = document.getElementById("newTaskInput");
  const list = document.getElementById("todoModalList");

  addBtn.addEventListener("click", () => {
    const task = input.value.trim();
    if (task !== "") {
      const li = document.createElement("li");
      li.textContent = task;
      list.appendChild(li);
      input.value = "";
      saveTasks(); // ←localStorage保存（次に作る）
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const openBtn = document.querySelector('.todo-widget-view');
  const modal = document.querySelector('.todo-modal');
  const taskInput = document.getElementById('newTaskInput');
  const addBtn = document.getElementById('addTodoBtn');
  const modalList = document.querySelector('.modal-todo-list');
  const widgetList = document.querySelector('.todo-display-list');

  // モーダル開く
  window.openToDoModal = function () {
    modal.style.display = 'flex';
  };

  // モーダル閉じる（任意で）
  window.closeToDoModal = function () {
    modal.style.display = 'none';
  };

  // タスク追加処理
  addBtn.addEventListener('click', () => {
    const task = taskInput.value.trim();
    if (task === '') return;

    // モーダル側に追加
    const modalItem = document.createElement('li');
    modalItem.textContent = task;
    modalList.appendChild(modalItem);

    // 表示ウィジェットにも追加（省略表現付き）
    const widgetItem = document.createElement('li');
    const span = document.createElement('span');
    span.className = 'check-circle';
    span.textContent = '○';

    const shortText = task.length > 6 ? task.slice(0, 6) + '…' : task;

    widgetItem.appendChild(span);
    widgetItem.appendChild(document.createTextNode(' ' + shortText));
    widgetList.appendChild(widgetItem);

    taskInput.value = '';
  });
});

<script>
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-modal-target]').forEach(widget => {
      widget.addEventListener('click', () => {
        const modalId = widget.getAttribute('data-modal-target');
        const modal = document.getElementById(modalId);
        if (modal) {
          modal.style.display = 'flex'; // 表示（flexにして中央表示）
        }
      });
    });

    // モーダルの外側クリックで閉じる（必要なら）
    document.addEventListener('click', (e) => {
      const modal = document.getElementById('todoModal');
      if (modal && e.target === modal) {
        modal.style.display = 'none';
      }
    });
  });
</script>
