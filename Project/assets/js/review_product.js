$('.star_review').each(function(star){
    $(this).on('click',function(){
        $(this).toggleClass('selected_star')
    });
})

const submit_product_review=document.querySelector('#submitreviewbutton')
if (submit_product_review!=null){
    submit_product_review.addEventListener('click', function (e) {
        e.preventDefault();
        var star=document.querySelector('.selected_star')
        if (star!=null){
            const data={
                product_id : this.getAttribute('product_id'),
                name : document.getElementById('id_reviewer_name').value,
                email : document.getElementById('id_reviewer_email').value,
                text: document.getElementById('id_review_text').value,
                star: document.querySelector('.selected_star').getAttribute('star_count'),
            }
            AddCommentLogin.AddComment(data)
            setTimeout(() => location.reload() , 500)

        }
        else{
            alert("Please select appropriate start count of your review")
        }

    })
}

const AddCommentLogin = {
    url: `${location.origin}/api/comments/create`,

    AddComment(data) {
        fetch(this.url, {
            method: 'POST',
            credentials:'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                'reviewer_name': data.name,
                'reviewer_email': data.email,
                'review_text': data.text,
                'product_id': data.product_id,
                'review_star': data.star,
            })

        }).then(response => response.json())
            
            

        
    }
}
