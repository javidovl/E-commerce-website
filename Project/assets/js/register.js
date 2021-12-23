
// button = document.getElementById('register-form-submit');
// if (button!=null){
//     button.addEventListener('click', function (e) {
//         e.preventDefault();
//         const data={
//             name : document.getElementById('id_register_name').value,
//             email : document.getElementById('id_register_email').value,
//             phone_number : document.getElementById('id_register_phone_number').value,
//             password : document.getElementById('id_register_password').value,
//             password_conf : document.getElementById('id_register_password_again').value
//         }
//         RegisterLogic.RegisterUser(data)
//         setTimeout(() => location.reload() , 500)
//     })
// }



// const RegisterLogic = {
//     url: `${location.origin}/api/accounts/create`,

//     RegisterUser(data) {
//         if (data.password != data.password_conf) {
//             alert("Password and password confirmation do not match")
//         }
//         else{
//             fetch(this.url, {
//                 method: 'POST',
//                 credentials:'include',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': getCookie('csrftoken'),
//                 },
//                 body: JSON.stringify({
//                     'name': data.name,
//                     'email': data.email,
//                     'phone_number': data.phone_number,
//                     'password': data.password
//                 })
    
//             }).then(response => response.json())
                
            
//         }

        
//     }
// }
