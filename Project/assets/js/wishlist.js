const WishListLogic = {
    url: `${location.origin}/api/wishlist/`,

    addToWishlist(product_version_id) {
        fetch(this.url, {
            method: 'POST',
            credentials:'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                
            },
            body: JSON.stringify({
                'product_version_id': product_version_id,
            })
        }).then(response => response.json()).then(data => {
            if (data.success){
                console.log(data.message);
            }
            else{
                alert(data.message);
            }
        })
        
    },
    checkStock(product_id,size,color) {
        fetch(`${location.origin}/api/product_version/`, {
            method: 'POST',
            credentials:'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                
            },
            body: JSON.stringify({
                'product_id': product_id,
                'size': size,
                'color': color,
            })
        }).then(response => response.json()).then(data => {
            if (data.success){
                // console.log(data.message)
            }
            else{
                WishListLogic.addToWishlist(data.product_version_id, document.querySelector(".quantity_of_product").value);
                alert(data.message);
            }
        })
        
    },

    deletefromwishlist(product_version_id){
        fetch(`${location.origin}/api/wishlist/`, {
            method: 'DELETE',
            credentials:'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                
            },
            body: JSON.stringify({
                'product_version_id': product_version_id})

            })
            .then(location.reload())
        }
            
}


document.querySelectorAll('.add_to_wishlist_button').forEach(button => {
    button.addEventListener('click', event => {
        product_id=button.getAttribute('product_id')
        size=$(".size_of_product").val()
        color=document.querySelector(".outline").getAttribute('color')
        WishListLogic.checkStock(product_id,size, color);

    })
})

document.querySelectorAll('.delete-product_item_from_wishlist_button').forEach(button => {
    button.addEventListener('click', event => {
        product_version_id=button.getAttribute('product_version_id')
        WishListLogic.deletefromwishlist(product_version_id);

    })
})
