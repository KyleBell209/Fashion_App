// Select all dropdown menu items and add a click event listener to each one
document.querySelectorAll('.dropdown-menu .dropdown-item').forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent the default click behavior

    // Get the current URL
    const url = new URL(window.location.href);

    // Determine whether the dropdown item is for a master category or sub category
    const paramName = e.target.parentElement.getAttribute('aria-labelledby') === 'dropdownMenuButton' ? 'master_category' : 'sub_category';

    // Set the query parameter for the selected category
    url.searchParams.set(paramName, e.target.textContent.trim() === 'All' ? '' : e.target.textContent.trim());

    // Redirect to the new URL with the updated query parameters
    window.location.href = url.toString();
  });
});
