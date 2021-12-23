const OrderLogic = {
    url: `${location.origin}/api/order/`,
    
    createOrder(user, basket_id, billing_address_id) {
        fetch(this.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                user_id: user,
                basket_id: basket_id,
                billing_address_id: billing_address_id
            })
        })
        .then(res => res.json())
        .then(res => {
            if (res.success) {
                console.log(res.message);
            }
            else{
                alert(res.message);
                console.log(res.order_id);
                window.location.replace(`${location.origin}/order-complete/${res.order_id}`);
            }
        })
    },
    // getOrder(order_id) {
    //     return fetch(`${this.url}${user}`)
    //     .then(res => res.json())
    //     .then(res => {
    //         if (res.success) {
    //             return res.data;
    //         }
    //         else{
    //             alert(res.message);
    //         }
    //     })
    // }

     
}


button=document.querySelector("#complete-order-button")
if (button!=null){
    button.addEventListener("click", ()=>{
        OrderLogic.createOrder(
            button.getAttribute("user"),
            $("#data-basket-id").val(),
            $("#data-address-id").val()

        )
    })
}