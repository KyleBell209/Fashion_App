document.addEventListener('DOMContentLoaded', function () {
  const masterCategory = document.getElementById('masterCategory');
  const subCategory = document.getElementById('subCategory');
  const articleType = document.getElementById('articleType');
  const gender = document.getElementById('gender');

  //Event listener to the gender field to listen for changes
  gender.addEventListener('change', refreshFilteredProducts);

  function filterOptionsByGender(options, genderRestrictions, selectedGender, selectedSubCategory) {
    return options.filter(option => {
      if (!genderRestrictions) {
        return true;
      }
  
      if (typeof genderRestrictions[selectedSubCategory] === 'boolean') {
        return genderRestrictions[selectedSubCategory] === false;
      } else if (Array.isArray(genderRestrictions[selectedSubCategory])) {
        return !genderRestrictions[selectedSubCategory].includes(option);
      }
      return true;
    });
  }

  // Men's restrictions
  const menRestrictions = {
    'Apparel': {
      'Dress': true,
      'Apparel Set': true,
      'Topwear': ['Tunics', 'Shrug'],
      'Bottomwear': ['Skirts', 'Stockings', 'Leggings', 'Capris'],
      'Loungewear and Nightwear': ['Nightdress', 'Robe', 'Lounge Tshirts']
    },
    'Accessories': {
      'Bags': ['Clutches', 'Trolley Bag', 'Mobile Pouch', 'Rucksacks', 'Tablet Sleeve', 'Trolley Bag']
    },
    'Footwear': {
      'Shoes': ['Heels', 'Flats']
    }
  };

  // Women's restrictions
  const womenRestrictions = {
    'Apparel': {
      'Topwear': ['Suspenders'],
      'Bottomwear': ['Rain Trousers']
    },
    'Accessories': {
      'Ties': true,
      'Gloves': true,
      'Cufflinks': true,
      'Sports Accessories': true,
      'Bags': ['Messenger Bag', 'Rucksacks', 'Trolley Bag', 'Waist Pouch']
    },
    'Footwear': {
      'Shoes': ['Formal Shoes']
    }
  };

  const apparelOptions = [
    'Topwear',
    'Bottomwear',
    'Dress',
    'Loungewear and Nightwear',
    'Apparel Set',
  ];

  const accessoriesOptions = [
    'Watches',
    'Belts',
    'Bags',
    'Jewellery',
    'Eyewear',
    'Headwear',
    'Ties',
    'Gloves',
    'Sports Accessories',
    'Cufflinks',
    'Stoles',
    'Scarves',
  ];

  const footwearOptions = ['Shoes', 'Flip Flops', 'Sandal'];
  const articleTypeOptions = {
    'Accessories': ['Accessory Gift Set', 'Key Chain'],
    'Apparel Set': ['Swimwear'],
    'Bags': ['Backpacks', 'Clutches', 'Duffel Bag', 'Handbags', 'Laptop Bag', 'Mobile Pouch', 'Messenger Bag', 'Rucksacks', 'Tablet Sleeve', 'Trolley Bag', 'Waist Pouch'],
    'Bottomwear': ['Capris', 'Jeans', 'Leggings', 'Rain Trousers', 'Shorts', 'Skirts', 'Stockings', 'Swimwear', 'Track Pants', 'Trousers'],
    'Cufflinks': ['Cufflinks', 'Cufflinks and Ties'],
    'Dresses': ['Dresses', 'Jumpsuit'],
    'Headwear': ['Cap', 'Hat', 'Headband'],
    'Jewellery': ['Bangle', 'Bracelet', 'Earrings', 'Jewellery Set', 'Necklace and Chains', 'Pendant', 'Ring'],
    'Loungewear and Nightwear': ['Lounge Pants', 'Lounge Shorts', 'Lounge Tshirts', 'Night suits', 'Nightdress', 'Robe', 'Shorts'],
    'Sandals': ['Sandals', 'Sports Sandals'],
    'Shoes': ['Casual Shoes', 'Flats', 'Formal Shoes', 'Heels', 'Sports Shoes'],
    'Topwear': ['Tops', 'Tshirts', 'Blazers', 'Jackets', 'Shirts', 'Shrug','Suspenders', 'Sweaters', 'Sweatshirts', 'Tunics', 'Waistcoat'],
  };

  function updateSubCategoryOptions(options) {
    subCategory.innerHTML = '<option value="">Select</option>';

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;
    
      subCategory.appendChild(optionElement);
    });
  }

  function updateArticleTypeOptions(options) {
    articleType.innerHTML = '<option value="">Select</option>';

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;
    
      articleType.appendChild(optionElement);
    });
  }

  function onMasterCategoryChange() {
    const selectedMasterCategory = masterCategory.value;
    let subCategoryOptions;
    const selectedGender = gender.value;
  
    if (selectedMasterCategory === 'Apparel') {
      subCategoryOptions = apparelOptions;
    } else if (selectedMasterCategory === 'Accessories') {
      subCategoryOptions = accessoriesOptions;
    } else if (selectedMasterCategory === 'Footwear') {
      subCategoryOptions = footwearOptions;
    } else {
      subCategory.innerHTML = '<option value="">Select</option>';
      articleType.innerHTML = '<option value="">Select</option>';
      return;
    }
  
    if (selectedGender === 'Men') {
      subCategoryOptions = filterOptionsByGender(subCategoryOptions, menRestrictions[selectedMasterCategory], selectedGender);
    } else if (selectedGender === 'Women') {
      subCategoryOptions = filterOptionsByGender(subCategoryOptions, womenRestrictions[selectedMasterCategory], selectedGender);
    }
  
    updateSubCategoryOptions(subCategoryOptions);
    articleType.innerHTML = '<option value="">Select</option>';
  }
  
  function onSubCategoryChange() {
    const selectedSubCategory = subCategory.value;
    let articleTypeOptionsForSubCategory;
    if (articleTypeOptions[selectedSubCategory]) {
      articleTypeOptionsForSubCategory = articleTypeOptions[selectedSubCategory];
    } else {
      articleType.innerHTML = '<option value="">Select</option>';
      return;
    }
  
    let restrictions;
    if (gender.value === 'Men' && menRestrictions[masterCategory.value] && menRestrictions[masterCategory.value][selectedSubCategory]) {
      restrictions = menRestrictions[masterCategory.value];
    } else if (gender.value === 'Women' && womenRestrictions[masterCategory.value] && womenRestrictions[masterCategory.value][selectedSubCategory]) {
      restrictions = womenRestrictions[masterCategory.value];
    } else {
      restrictions = gender.value === 'Men' ? menRestrictions : womenRestrictions;
    }
  
    articleTypeOptionsForSubCategory = filterOptionsByGender(articleTypeOptionsForSubCategory, restrictions, gender.value, selectedSubCategory);
    updateArticleTypeOptions(articleTypeOptionsForSubCategory);
  }
  
  masterCategory.addEventListener('change', onMasterCategoryChange);
  subCategory.addEventListener('change', onSubCategoryChange);
  
  if (user_preferences.masterCategory) {
    masterCategory.value = user_preferences.masterCategory;
    onMasterCategoryChange();
  }
  
  if (user_preferences.subCategory) {
    subCategory.value = user_preferences.subCategory;
    onSubCategoryChange();
  }
  
  gender.addEventListener('change', function () {
    onMasterCategoryChange();
    onSubCategoryChange();
  });
});
    
    // Get the form and form fields
    const form = document.getElementById('preferences-form');
    const formFields = Array.from(form.elements).filter(el => el.tagName === 'SELECT');
  
    // Function to refresh the filtered products
    function refreshFilteredProducts() {
      const hasSelectedValue = formFields.some(field => field.value !== "");

      if (!hasSelectedValue) {
        const filteredProducts = document.getElementById('filtered-products');
        filteredProducts.innerHTML = '';
        return;
      }
      
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
          attachAddToCartEventListeners();
        });
      }
      
      function handleFormSubmit(event) {
        event.preventDefault();
      }
      
      form.addEventListener('submit', handleFormSubmit);
      
      // Add an event listener to the form fields to listen for changes
      formFields.forEach(field => {
        field.addEventListener('change', refreshFilteredProducts);
      });
      
    // Add an event listener to the form fields to listen for changes
    formFields.forEach(field => {
      field.addEventListener('change', refreshFilteredProducts);
    });
  
    // Add a click event listener for the "More products?" button
    document.getElementById('more-products').addEventListener('click', refreshFilteredProducts);
  
    // Call the refreshFilteredProducts function initially to load the products
    refreshFilteredProducts();
    

    function attachAddToCartEventListeners() {
      document.querySelectorAll('.update-cart').forEach(button => {
        button.addEventListener('click', function (event) {
          event.preventDefault(); // Add this line to prevent the form submission
          const productId = event.target.getAttribute('data-product');
          const action = event.target.getAttribute('data-action');
          const source = event.target.getAttribute('data-source') || '';
          console.log(`Product ID: ${productId}, Action: ${action}, Source: ${source}`);
    
          if (user == 'AnonymousUser') {
            console.log('User is not authenticated');
          } else {
            updateUserOrder(productId, action, source, event);
          }
        });
      });
    }

  function updateUserOrder(productId, action, source, event) {
    event.preventDefault();
  
    fetch('/update_item/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({'productId': productId, 'action': action, 'source': source})
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log('data:', data);
    });
  }
  
  

  document.addEventListener('DOMContentLoaded', function () {
    attachAddToCartEventListeners();
  });

    
    
    