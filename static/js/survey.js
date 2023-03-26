document.addEventListener('DOMContentLoaded', function () {
  const masterCategory = document.getElementById('masterCategory');
  const subCategory = document.getElementById('subCategory');

  const apparelOptions = [
    'Topwear',
    'Bottomwear',
    'Saree',
    'Dress',
    'Loungewear and Nightwear',
    'Apparel Set',
  ];

  const accessoriesOptions = [
    'Watches',
    'Belts',
    'Bags',
    'Shoe Accessories',
    'Jewellery',
    'Eyewear',
    'Headwear',
    'Mufflers',
    'Ties',
    'Gloves',
    'Sports Accessories',
    'Cufflinks',
    'Stoles',
    'Scarves',
  ];

  const footwearOptions = ['Shoes', 'Flip Flops', 'Sandal'];

  function updateSubCategoryOptions(options) {
    subCategory.innerHTML = '<option value="">Select</option>';

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;

      if (user_preferences.subCategory === option) {
        optionElement.selected = true;
      }

      subCategory.appendChild(optionElement);
    });
  }

  function onMasterCategoryChange() {
    if (masterCategory.value === 'Apparel') {
      updateSubCategoryOptions(apparelOptions);
    } else if (masterCategory.value === 'Accessories') {
      updateSubCategoryOptions(accessoriesOptions);
    } else if (masterCategory.value === 'Footwear') {
      updateSubCategoryOptions(footwearOptions);
    } else {
      subCategory.innerHTML = '<option value="">Select</option>';
    }
  }

  masterCategory.addEventListener('change', onMasterCategoryChange);

  if (masterCategory.value !== '') {
    onMasterCategoryChange();
  }
});
    
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


