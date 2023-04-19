// This function returns a new function that will only execute after a certain amount of time has passed since the last time it was called.
// This is useful for situations where we want to debounce user input, such as when they're typing in a search box.
function debounce(func, wait) {
    let timeout;

    return function () {
        const context = this,
            args = arguments;

        clearTimeout(timeout);

        timeout = setTimeout(function () {
            timeout = null;
            func.apply(context, args);
        }, wait);
    };
}

// Get all the update buttons on the page.
var updateBtns = document.getElementsByClassName('update-likes');

// This function refreshes the page with a delay of `delay` milliseconds.
function refreshPageWithDelay(delay) {
    setTimeout(() => {
        location.reload();
    }, delay);
}

// Add event listeners to all the update buttons that debounce the click event.
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', debounce(function () {
        // Get the product ID and action associated with the clicked button.
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var source = this.dataset.source || '';

        // Log some information about the click event.
        console.log('FashionProductID:', productId, 'UserAction:', action);
        console.log('From User ', user);

        // If the user is not logged in, show a message in the console.
        if (user == 'AnonymousUser') {
            console.log('NOT LOGGED IN!');
        } else {
            // Otherwise, call the `updateLike` function to update the product's like count.
            updateLike(productId, action, source);
        }
    }, 500));
}

// This function sends a POST request to update the like count for a product.
function updateLike(productId, action, source) {
    console.log("SUCCESS!");

    // Define the URL and request headers.
    var url = "/update_like/";
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        // Define the request body as a JSON object.
        body: JSON.stringify({ productId: productId, action: action, source: source }),
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            // If the action was a "superlike", update the button's styling to reflect the change.
            if (action === "superlike") {
                const superlikeBtn = document.querySelector(
                    `button[data-product="${productId}"][data-action="superlike"][data-source="${source}"]`
                );
                if (superlikeBtn) {
                    if (data.superliked) {
                        superlikeBtn.classList.remove("btn-outline-primary");
                        superlikeBtn.classList.add("superlike-active");
                    } else {
                        superlikeBtn.classList.remove("superlike-active");
                        superlikeBtn.classList.add("btn-outline-primary");
                    }
                }
            }
            // Refresh the page with a delay of 500ms after the like count has been updated.
            refreshPageWithDelay(500);
        });
}

// This function sends a POST request to delete the user's account.
function deleteAccount() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/delete_account/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onreadystatechange = function () {
        // If the request was// successful, redirect the user to the homepage.
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.href = '/';
        }
    };
    xhr.send();
}
