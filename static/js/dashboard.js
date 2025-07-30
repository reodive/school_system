document.addEventListener("DOMContentLoaded", function () {
    const pageType = document.body.dataset.pageType;  // ページの種類を取得

    if (pageType === "teacher") {
        loadTeacherDashboard();
    } else if (pageType === "student") {
        loadStudentDashboard();
    }

    function loadTeacherDashboard() {
        var ctx = document.getElementById('submissionChart')?.getContext('2d');
        if (!ctx) return;

        var labels = JSON.parse(document.getElementById('chart-data').dataset.labels);
        var submittedData = JSON.parse(document.getElementById('chart-data').dataset.submitted);
        var pendingData = JSON.parse(document.getElementById('chart-data').dataset.pending);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: '提出済み',
                        data: submittedData,
                        backgroundColor: 'rgba(75, 192, 192, 0.8)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                    },
                    {
                        label: '未提出',
                        data: pendingData,
                        backgroundColor: 'rgba(255, 99, 132, 0.8)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                    }
                ]
            },
            options: {
                responsive: true,
                animation: { duration: 1000, easing: 'easeOutBounce' },
                scales: { y: { beginAtZero: true } }
            }
        });

        updateNotifications();
        setInterval(updateNotifications, 60000);
    }

    function loadStudentDashboard() {
        var ctx = document.getElementById('progressChart')?.getContext('2d');
        if (!ctx) return;

        var labels = JSON.parse(document.getElementById('chart-data').dataset.labels);
        var completedData = JSON.parse(document.getElementById('chart-data').dataset.completed);
        var remainingData = JSON.parse(document.getElementById('chart-data').dataset.remaining);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: '完了',
                        data: completedData,
                        backgroundColor: ['rgba(54, 162, 235, 0.8)', 'rgba(255, 206, 86, 0.8)'],
                        borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'],
                        borderWidth: 2
                    }
                ]
            },
            options: { responsive: true }
        });
    }

    function updateNotifications() {
        fetch("/api/get_notifications/")
            .then(response => response.json())
            .then(data => {
                const stream = document.getElementById('activity-stream');
                if (!stream) return;
                stream.innerHTML = '';
                data.notifications.forEach(notification => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item';
                    li.textContent = notification.message;
                    stream.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching notifications:', error));
    }
});
document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const editBtn = document.querySelector('.edit-floating');

  // 編集モードの切替
  editBtn && editBtn.addEventListener('click', () => {
    body.classList.toggle('edit-mode');
    editBtn.innerText = body.classList.contains('edit-mode') ? '完了' : 'ウィジェットを編集';
  });

  // サイズボタンのクリック処理
  document.querySelectorAll('.widget-toolbar button').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const widget = btn.closest('.widget');
      const size = btn.dataset.size;

      // クラスを上書き
      widget.classList.remove('size-small', 'size-medium', 'size-large');
      widget.classList.add(`size-${size}`);

      // ツールバーのボタン状態更新
      btn.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
});
