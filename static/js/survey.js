    // Get the form and form fields
    const form = document.getElementById('preferences-form');
    const formFields = Array.from(form.elements).filter(el => el.tagName === 'SELECT');
  
    // Function to refresh the filtered products
    function refreshFilteredProducts() {
      // Get the form data and make an AJAX request to the server to get the filtered products
      const formData = new FormData(form);
      fetch('/get_filtered_products/', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          // Replace the filtered products section with the new products
          const filteredProducts = document.getElementById('filtered-products');
          if (data.length) {
            filteredProducts.innerHTML = data.map(product => `
                <div class="col-6 col-md-4 col-lg-3">
                    <div class="card mb-4">
                        <img src="${product.image_url}" class="card-img-top">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <button data-product="${product.id}" data-action="add" class="btn btn-primary update-cart">Add to Cart</button>
                        </div>
                    </div>
                </div>
            `).join('');
          } else {
            filteredProducts.innerHTML = '<p>No Clothing Found</p>';
          }
        });
    }
  
    // Add an event listener to the form fields to listen for changes
    formFields.forEach(field => {
      field.addEventListener('change', refreshFilteredProducts);
    });
  
    // Add a click event listener for the "More products?" button
    document.getElementById('more-products').addEventListener('click', refreshFilteredProducts);
  
    // Call the refreshFilteredProducts function initially to load the products
    refreshFilteredProducts();