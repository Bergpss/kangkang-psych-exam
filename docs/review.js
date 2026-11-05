'use strict';
document.querySelectorAll('.model-id').forEach(function (button) {
  button.addEventListener('click', function () {
    const revealed = button.classList.toggle('revealed');
    const model = button.dataset.model || '';
    button.setAttribute('aria-expanded', String(revealed));
    button.setAttribute('aria-label', revealed
      ? '模型 ID：' + model + '；再次点击隐藏'
      : '模型 ID 已模糊，点击显示');
  });
});
