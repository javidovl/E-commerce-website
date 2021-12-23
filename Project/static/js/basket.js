const BasketLogic = {
    url: `${location.origin}/api/product_version/`,

    checkStock(product_id,size,color) {
        fetch(this.url, {
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
            }
            else{
                BasketLogic.addToBasket(data.product_version_id, document.querySelector(".quantity_of_product").value);
            }
        })
        
    },

    addToBasket(product_version_id,quantity) {
        fetch(`${location.origin}/api/basket/`, {
            method: 'POST',
            credentials:'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                
            },
            body: JSON.stringify({
                'product_version_id': product_version_id,
                'quantity': quantity,
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



    getBasket(){
        const url = new URL(location.origin + '/api/basket/');
        fetch(url).then(response => response.json()).then(data => 
            BasketLogic.setBasket(data))
            
        
    
    },
    setBasket(data){
        document.querySelector('.cartdrop-items').innerHTML=""
        for (var i = data.product_list[0]; i <= data.product_list.slice(-1).pop(); i++){   //getting first and last basket item id
            item=data.product_features[i]
            if (item!=null){
                $('.cartdrop-items').append(`<div class="sin-itme clearfix">
            <i class="mdi mdi-close delete-basket-item-button" basket_item_id=${i}></i>
            <a class="cart-img" href="{% url 'cart' %}"><img src="${item[5]}" alt="" /></a>
            <div class="menu-cart-text">
                <a href="#"><h5>${item[0]}</h5></a>
                <span>Color : ${item[3]} </span>
                <span>Size :   ${item[2]}  </span>
                <span>Quantity : ${item[4]}</span>
                <strong>$${item[1]}</strong>
            </div>
            </div>`)
            }
            
        }
       BasketLogic.updateNumbers(data)
       location.reload()
        
        
    },
    updateNumbers(data){
        number_of_items=Object.keys(data.product_list).length
        $(".number_of_items_in_card").text(number_of_items)
        $('.total_price_of_basket').text(`$${data.total_price}`);
    }, 

    deleteItem(basket_item_id){
        fetch(`${location.origin}/api/basket/delete_item`, {
            method: 'DELETE',
            credentials:'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                
            },
            body: JSON.stringify({
                'basket_item_id': basket_item_id})

            })
        }
            

}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
       var c = ca[i];
       while (c.charAt(0)==' ') c = c.substring(1);
       if(c.indexOf(name) == 0)
          return c.substring(name.length,c.length);
    }
    return "";
}


document.querySelectorAll('.add_to_card_button').forEach(button => {
    button.addEventListener('click', event => {
        product_id=button.getAttribute('product_id')
        size=$(".size_of_product").val()
        color=document.querySelector(".outline").getAttribute('color')

        BasketLogic.checkStock(product_id, size, color);
        setTimeout(() => {BasketLogic.getBasket()} , 500);      

    })
})




deletebuttons=document.querySelectorAll('.delete-basket-item-button')
        
document.querySelectorAll('.delete-basket-item-button').forEach(button => {
    button.addEventListener('click', event => {
        basket_item_id=button.getAttribute('basket_item_id')
        BasketLogic.deleteItem(basket_item_id);
        setTimeout(() => {BasketLogic.getBasket()} , 500);

    })
    
})

document.querySelectorAll('.add_to_card_button_wishlist').forEach(button => {
    button.addEventListener('click', event => {
        product_version_id=button.getAttribute('product_version_id')
        BasketLogic.addToBasket(product_version_id,1);
        WishListLogic.deletefromwishlist(product_version_id);
        setTimeout(() => {BasketLogic.getBasket()} , 500);      

    })
})





