var updateBtns = document.getElementsByClassName('update-likes')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var source = this.dataset.source || ''; 
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        if (user == 'AnonymousUser'){
            console.log('NOT LOGGED IN!')
        } else {
            updateUserOrder(productId, action, source)
        }
    })
}

function updateUserOrder(productId, action, source){
    console.log('SUCCESS!')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action, 'source': source})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        if (data.action === 'superlike') {
            // Get the superlike button element for the product
            const superlikeBtn = document.querySelector(`button[data-product="${data.productId}"][data-action="superlike"]`);
    
            if (data.superliked) {
                alert(data.message);
                superlikeBtn.classList.remove('btn-outline-primary');
                superlikeBtn.classList.add('superlike-active'); // Update this line
            } else {
                superlikeBtn.classList.remove('superlike-active'); // Update this line
                superlikeBtn.classList.add('btn-outline-primary');
            }
        } else {
            location.reload();
        }
    });
    
}

