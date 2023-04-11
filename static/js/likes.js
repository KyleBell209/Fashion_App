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

var updateBtns = document.getElementsByClassName('update-likes');

function refreshPageWithDelay(delay) {
    setTimeout(() => {
        location.reload();
    }, delay);
}

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', debounce(function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var source = this.dataset.source || '';
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);

        if (user == 'AnonymousUser') {
            console.log('NOT LOGGED IN!');
        } else {
            updateLike(productId, action, source);
        }
    }, 500));
}

function updateLike(productId, action, source) {
    console.log("SUCCESS!");

    var url = "/update_like/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({productId: productId, action: action, source: source}),
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
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
            refreshPageWithDelay(500);
        });
}

function deleteAccount() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/delete_account/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.href = '/';
        }
    };
    xhr.send();
}