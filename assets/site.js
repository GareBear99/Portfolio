(function () {
  const filterButtons = Array.from(document.querySelectorAll('[data-filter]'));
  const cards = Array.from(document.querySelectorAll('[data-project-category]'));
  const searchInput = document.getElementById('project-search');
  const status = document.getElementById('project-search-status');

  function applyFilters() {
    const active = document.querySelector('[data-filter].primary');
    const target = active ? active.dataset.filter : 'all';
    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
    let visible = 0;

    cards.forEach(card => {
      const matchesCategory = target === 'all' || card.dataset.projectCategory === target;
      const haystack = [card.dataset.projectCategory || '', card.textContent || ''].join(' ').toLowerCase();
      const matchesQuery = !query || haystack.includes(query);
      const show = matchesCategory && matchesQuery;
      card.style.display = show ? '' : 'none';
      if (show) visible += 1;
    });

    if (status) {
      if (!cards.length) {
        status.textContent = 'No project cards found on this page.';
      } else if (!query && target === 'all') {
        status.textContent = `Showing all ${visible} projects.`;
      } else {
        status.textContent = `Showing ${visible} project${visible === 1 ? '' : 's'} for ${target === 'all' ? 'all categories' : target}${query ? ` matching “${query}”` : ''}.`;
      }
    }
  }

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => b.classList.remove('primary'));
      btn.classList.add('primary');
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }

  applyFilters();
})();
