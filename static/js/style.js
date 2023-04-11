document.querySelectorAll('.dropdown-menu .dropdown-item').forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const url = new URL(window.location.href);
      const paramName = e.target.parentElement.getAttribute('aria-labelledby') === 'dropdownMenuButton' ? 'master_category' : 'sub_category';
      url.searchParams.set(paramName, e.target.textContent.trim() === 'All' ? '' : e.target.textContent.trim());
      window.location.href = url.toString();
    });
  });
