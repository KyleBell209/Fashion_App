var updateBtns = document.getElementsByClassName('update-likes')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var source = this.dataset.source || ''; // Add this line to get the source attribute
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        if (user == 'AnonymousUser'){
            console.log('NOT LOGGED IN!')
        } else {
            updateUserOrder(productId, action, source) // Pass the source attribute
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
        location.reload()
    });
}

