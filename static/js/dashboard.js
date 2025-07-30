document.addEventListener('DOMContentLoaded', () => {
  // ─── 追加する一行 ───────────────────
  document.querySelectorAll('.widget-box').forEach(box => box.classList.remove('editing'));
  // ────────────────────────────────────

  // 以降、既存の初期化／トグル処理
  const toggleBtn = document.getElementById('editModeToggle');
  let editing = false;
  // …（省略）…
});
document.addEventListener('DOMContentLoaded', () => {
  // ─── Charts ─────────────────────────────────────────────
  const pageType = document.body.dataset.pageType;
  if (pageType === 'teacher') {
    loadTeacherDashboard();
  } else if (pageType === 'student') {
    loadStudentDashboard();
  }

  // ─── 編集モード切替 ────────────────────────────────────
  const editBtn = document.getElementById('editModeToggle') || document.querySelector('.edit-floating');
  const dashboard = document.querySelector('.dashboard-grid');
  let editing = false;

  if (editBtn && dashboard) {
    // 初期はOFF
    dashboard.classList.remove('edit-mode');
    editBtn.innerText = 'ウィジェットを編集';

    editBtn.addEventListener('click', () => {
      editing = !editing;
      dashboard.classList.toggle('edit-mode', editing);
      editBtn.innerText = editing ? '完了' : 'ウィジェットを編集';
    });
  }

  // ─── サイズ変更ボタン ────────────────────────────────────
  document.querySelectorAll('.widget-toolbar button[data-size]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const widget = btn.closest('.widget-box');
      const size = btn.dataset.size;
      widget.classList.remove('size-small','size-medium','size-large');
      widget.classList.add(`size-${size}`);
      btn.closest('.widget-toolbar')
         .querySelectorAll('button[data-size]')
         .forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // ─── 削除ボタン ────────────────────────────────────────
  document.querySelectorAll('.widget-delete').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      btn.closest('.widget-box').remove();
    });
  });

  // ─── Sortable.js ───────────────────────────────────────
  if (typeof Sortable !== 'undefined' && dashboard) {
    new Sortable(dashboard, {
      handle: '.widget-box',
      animation: 150,
      ghostClass: 'dragging',
      dragClass: 'drag-active',
      chosenClass: 'drag-chosen',
      filter: '.widget-toolbar',
      onEnd: () => {
        console.log('New order:', [...dashboard.children].map(w => w.dataset.widgetName));
      }
    });
  }


  // ─── 以下、Dashboard チャート・通知周りの関数定義 ───────

  function loadTeacherDashboard() {
    const canvas = document.getElementById('submissionChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dataEl = document.getElementById('chart-data');
    const labels = JSON.parse(dataEl.dataset.labels);
    const submitted = JSON.parse(dataEl.dataset.submitted);
    const pending   = JSON.parse(dataEl.dataset.pending);

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          { label:'提出済み', data:submitted, backgroundColor:'rgba(75,192,192,0.8)', borderColor:'rgba(75,192,192,1)', borderWidth:2, borderRadius:8 },
          { label:'未提出',   data:pending,   backgroundColor:'rgba(255,99,132,0.8)', borderColor:'rgba(255,99,132,1)', borderWidth:2, borderRadius:8 }
        ]
      },
      options: {
        responsive:true,
        animation:{ duration:1000, easing:'easeOutBounce' },
        scales:{ y:{ beginAtZero:true }}
      }
    });

    updateNotifications();
    setInterval(updateNotifications, 60000);
  }

  function loadStudentDashboard() {
    const canvas = document.getElementById('progressChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dataEl     = document.getElementById('chart-data');
    const labels     = JSON.parse(dataEl.dataset.labels);
    const completed  = JSON.parse(dataEl.dataset.completed);
    const remaining  = JSON.parse(dataEl.dataset.remaining);

    new Chart(ctx, {
      type:'doughnut',
      data:{
        labels,
        datasets:[{
          label:'完了',
          data:completed,
          backgroundColor:['rgba(54,162,235,0.8)','rgba(255,206,86,0.8)'],
          borderColor:['rgba(54,162,235,1)','rgba(255,206,86,1)'],
          borderWidth:2
        }]
      },
      options:{ responsive:true }
    });
  }

  function updateNotifications() {
    fetch('/api/get_notifications/')
      .then(res=>res.json())
      .then(data=>{
        const stream = document.getElementById('activity-stream');
        if (!stream) return;
        stream.innerHTML = '';
        data.notifications.forEach(n => {
          const li = document.createElement('li');
          li.className = 'list-group-item';
          li.textContent = n.message;
          stream.appendChild(li);
        });
      })
      .catch(err=>console.error(err));
  }
});
document.addEventListener('DOMContentLoaded', () => {
  const editBtn = document.getElementById('editModeToggle'); // ボタン
  const target = document.body; // あるいは document.querySelector('.dashboard-grid')

  // 初期は編集モードOFF
  target.classList.remove('edit-mode');
  editBtn.innerText = 'ウィジェットを編集';

  editBtn.addEventListener('click', () => {
    const isEditing = target.classList.toggle('edit-mode');
    editBtn.innerText = isEditing ? '完了' : 'ウィジェットを編集';
  });
});
