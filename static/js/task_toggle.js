document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.todo__item input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', async () => {
      const li = checkbox.closest('.todo__item');
      const taskId = li.dataset.taskId;
      try {
        const res = await fetch(`/tasks/${taskId}/toggle/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
          },
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Toggle failed');
        // 見た目を微調整（✓入れ替えなど）
        li.classList.toggle('completed', data.done);
      } catch (err) {
        console.error(err);
        alert('タスクの更新に失敗しました');
        // 元に戻す
        checkbox.checked = !checkbox.checked;
      }
    });
  });
});

document.querySelector('meta[name="csrf-token"]').content
