document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', "{% url 'users:signup' %}", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.error_message) {
                    var errorMessageContainer = document.getElementById('error-message');
                    if (errorMessageContainer) {
                        errorMessageContainer.textContent = response.error_message;
                    }
                } else if (response.email_message) {
                    var emailMessageContainer = document.getElementById('email-message');
                    if (emailMessageContainer) {
                        emailMessageContainer.textContent = response.email_message;
                    }
                } else if (response.password_message) {
                    var passwordMessageContainer = document.getElementById('password-message');
                    if (passwordMessageContainer) {
                        passwordMessageContainer.textContent = response.password_message;
                    }
                } else {
                    window.location.href = "{% url 'users:signin' %}";
                }
            } else {
                console.error('Request error:', xhr.status);
            }
        }
    };
    xhr.send(formData);
});