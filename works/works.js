(() => {
  const search = document.getElementById('work-search');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const entries = [...document.querySelectorAll('.work-entry')];
  const count = document.getElementById('result-count');
  const empty = document.getElementById('empty-state');
  let category = 'all';

  const normalize = (value) => value.normalize('NFKC').toLocaleLowerCase()
    .replace(/[\p{P}\p{S}]+/gu, ' ').replace(/\s+/g, ' ').trim();
  const searchIndex = new Map(entries.map((entry) => [
    entry, normalize(`${entry.textContent} ${entry.dataset.search || ''}`),
  ]));

  const update = () => {
    const query = normalize(search?.value || '');
    let visible = 0;

    entries.forEach((entry) => {
      const matchesCategory = category === 'all' || entry.dataset.category === category;
      const matchesQuery = !query || searchIndex.get(entry).includes(query);
      const matches = matchesCategory && matchesQuery;
      entry.hidden = !matches;
      if (matches) visible += 1;
    });

    if (count) count.textContent = `${visible} ${visible === 1 ? 'project' : 'projects'} shown`;
    if (empty) empty.hidden = visible !== 0;
  };

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      category = button.dataset.filter || 'all';
      buttons.forEach((item) => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      update();
    });
  });

  search?.addEventListener('input', update);
  update();
})();
