// Wait for the DOM content to load before executing the function
document.addEventListener('DOMContentLoaded', function () {
  // Get DOM elements
  const masterCategory = document.getElementById('masterCategory');
  const subCategory = document.getElementById('subCategory');
  const articleType = document.getElementById('articleType');
  const gender = document.getElementById('gender');

  // Add event listener for when the gender value changes
  gender.addEventListener('change', refreshFilteredProducts);

  // Function to filter options by gender
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
  // Men's and women's clothing restrictions
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
  // Apparel category options
  const apparelOptions = [
    'Topwear',
    'Bottomwear',
    'Dress',
    'Loungewear and Nightwear',
    'Apparel Set',
  ];
  // Accessory category options
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
  // footwear category options
  const footwearOptions = ['Shoes', 'Flip Flops', 'Sandal'];
  // articleTypeOptions options
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
    'Topwear': ['Tops', 'Tshirts', 'Blazers', 'Jackets', 'Shirts', 'Shrug', 'Suspenders', 'Sweaters', 'Sweatshirts', 'Tunics', 'Waistcoat'],
  };

  // Update the subcategory options based on the selected category
  function updateSubCategoryOptions(options) {
    subCategory.innerHTML = '<option value="">Select</option>';

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;

      subCategory.appendChild(optionElement);
    });
  }
  // Update the article type options based on the selected subcategory
  function updateArticleTypeOptions(options) {
    articleType.innerHTML = '<option value="">Select</option>';

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;

      articleType.appendChild(optionElement);
    });
  }
  // Event handler for when the master category changes
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
  // Event handler for when the subcategory changes
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
  // event listeners for changes in master and sub categories
  masterCategory.addEventListener('change', onMasterCategoryChange);
  subCategory.addEventListener('change', onSubCategoryChange);
  // Initialize user preferences
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

const form = document.getElementById('preferences-form');
const formFields = Array.from(form.elements).filter(el => el.tagName === 'SELECT');

// Refresh the filtered products based on form data
function refreshFilteredProducts() {
  const hasSelectedValue = formFields.some(field => field.value !== "");

  if (!hasSelectedValue) {
    const filteredProducts = document.getElementById('filtered-products');
    filteredProducts.innerHTML = '';
    return;
  }

  const formData = new FormData(form);

  // Set empty preferences for all select fields with "Select" as their value
  formFields.forEach(field => {
    if (field.value === "") {
      formData.set(field.name, "");
    }
  });

  if (!hasSelectedValue) {
    user.preferences = "";
  } else {
    fetch('/get_filtered_products/', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        const filteredProducts = document.getElementById('filtered-products');
        if (data.length) {
          filteredProducts.innerHTML = data.map(product => `
              <div class="col-6 col-md-4 col-lg-3">
                <div class="card mb-4">
                  <img src="${product.image_url}" class="card-img-top">
                  <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <button data-product="${product.id}" data-action="add" class="btn btn-outline-secondary add-btn update-likes">Add to Likes</button>
                    <button data-product="${product.id}" data-action="superlike" class="btn btn-outline-primary superlike-btn update-likes">Superlike</button>
                  </div>
                </div>
              </div>
            `).join('');
        } else {
          filteredProducts.innerHTML = '<p>No Clothing Found</p>';
        }        
        attachAddTolikesEventListeners();
      });
  }
}
// Update user preferences based on the current form data
function updateUserPreferences() {
  // Set user.preferences to empty string if all select fields are "Select"
  if (formFields.every(field => field.value === "")) {
    user.preferences = "";
  } else {
    // Set user.preferences with the current field values
    user.preferences = formFields.reduce((preferences, field) => {
      preferences[field.name] = field.value;
      return preferences;
    }, {});
  }
}
//  event listeners for updating user preferences
gender.addEventListener('change', function () {
  updateUserPreferences();
  onMasterCategoryChange();
  onSubCategoryChange();
});
usage.addEventListener('change', function () {
  updateUserPreferences();
  refreshFilteredProducts();
});
season.addEventListener('change', function () {
  updateUserPreferences();
  refreshFilteredProducts();
});
masterCategory.addEventListener('change', function () {
  updateUserPreferences();
  onMasterCategoryChange();
  refreshFilteredProducts();
});
subCategory.addEventListener('change', function () {
  updateUserPreferences();
  onSubCategoryChange();
  refreshFilteredProducts();
});
articleType.addEventListener('change', function () {
  updateUserPreferences();
  refreshFilteredProducts();
});

// Set user.preferences to empty string if all select fields are "Select"
if (formFields.every(field => field.value === "")) {
  user.preferences = "";
}

// Prevent form submission, as we are handling it with AJAX
function handleFormSubmit(event) {
  event.preventDefault();
}
//  form submit event listener
form.addEventListener('submit', handleFormSubmit);

//  event listeners for refreshing filtered products
formFields.forEach(field => {
  field.addEventListener('change', refreshFilteredProducts);
});

formFields.forEach(field => {
  field.addEventListener('change', refreshFilteredProducts);
});

document.getElementById('more-products').addEventListener('click', refreshFilteredProducts);

refreshFilteredProducts();

// Attach event listeners for adding items to likes or superlike
function attachAddTolikesEventListeners() {
  document.querySelectorAll('.add-btn, .superlike-btn').forEach(button => {
    button.addEventListener('click', function (event) {
      event.preventDefault(); 
      const productId = event.target.getAttribute('data-product');
      const action = event.target.getAttribute('data-action');
      const source = event.target.getAttribute('data-source') || '';
      console.log(`Product ID: ${productId}, Action: ${action}, Source: ${source}`);

      if (user == 'AnonymousUser') {
        console.log('User is not authenticated');
      } else {
        updateLike(productId, action, source, event);
      }
    });
  });
}
// Update the like status for a product
function updateLike(productId, action, source, event) {
  event.preventDefault();

  fetch('/update_like/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'productId': productId, 'action': action, 'source': source })
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let superliked = false;
      if (action === "superlike" && data.superliked) {
          superliked = true;
          location.reload();
      }
  
      const response_data = {
          message: superliked ? `Superliked ${productId}` : "Item was added",
          productId: productId,
          superliked: superliked,
      };
  
      if (action === "superlike") {
          const superlikeBtn = document.querySelector(
              `button[data-product="${productId}"][data-action="superlike"]`
          );
  
          if (data.superliked) {
              superlikeBtn.classList.remove("btn-outline-primary");
              superlikeBtn.classList.add("superlike-active");
          } else {
              superlikeBtn.classList.remove("superlike-active");
              superlikeBtn.classList.add("btn-outline-primary");
          }
      } else {
          location.reload();
      }
  });
}
// Attach event listeners for add to likes and superlike buttons
document.addEventListener('DOMContentLoaded', function () {
  attachAddTolikesEventListeners();
});
// Clear user preferences and reload the page
function clearPreferences() {
  // Send an AJAX request to the server to clear the user's preferences
  fetch('/clear_preferences/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({})
  })
  .then(response => response.json())
  .then(data => {
    console.log('Preferences cleared successfully');
    // Reload the page to update the filtered products
    location.reload();
  })
  .catch(error => {
    console.error('Error clearing preferences:', error);
  });
}
// Add event listener for clearing preferences button
document.getElementById('clear-preferences-btn').addEventListener('click', clearPreferences);
