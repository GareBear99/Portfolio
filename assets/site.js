document.querySelectorAll('[data-filter]').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(b => b.classList.remove('primary'));
    btn.classList.add('primary');
    document.querySelectorAll('[data-project-category]').forEach(card => {
      card.style.display = (target === 'all' || card.dataset.projectCategory === target) ? '' : 'none';
    });
  });
});