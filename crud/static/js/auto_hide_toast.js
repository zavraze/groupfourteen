setTimeout(() =>{
    const successMessage = document.getElementById('toast-success');
    const errorMessage = document.getElementById('toast-error');
    if (successMessage){
        successMessage.style.display = 'none';
    }

    if (errorMessage){
        errorMessage.style.display = 'none';
    }
}, 3000);