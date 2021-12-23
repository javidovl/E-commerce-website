const LoginLogic = {
    url: `${location.origin}/api/token/`,
    
    fetchToken(email, password) {
        fetch(this.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(res => res.json())
        .then(res => {
            if (res.access) {
                localStorage.setItem('token', res.access);
            }
            else{
                alert(res.message);
            }
        })
    }
     
}

function submitform(form){
    form.submit();
}
    
const submit= document.getElementById('login-form-submit');
const form = document.getElementById('loginform');


if (submit!=null){
    submit.onclick = function (event){
        event.preventDefault();
        const email = document.querySelector('#id_login_email').value;
        const password = document.querySelector('#id_login_password').value;
        LoginLogic.fetchToken(email, password);
        setTimeout(() => {submitform(form)} , 1000);         
    }
}