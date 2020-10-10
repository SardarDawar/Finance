const contactName = document.getElementById('contact-name')
const contactEmail = document.getElementById('contact-email')
const contactSubject = document.getElementById('contact-subject')
const contactMessage = document.getElementById('contact-message')

function checkContactForm() 
{
    if (contactName) {
        if (contactName.value.length < 1 || contactName.value.length > 50) return false;
    }
    else return false;
    if (contactEmail) {
        if (contactEmail.value.length < 1 || contactEmail.value.length > 100) return false;
    }
    else return false;
    if (contactSubject) {
        if (contactSubject.value.length < 1 || contactSubject.value.length > 150) return false;
    }
    else return false;
    if (contactMessage) {
        if (contactMessage.value.length < 1 || contactMessage.value.length > 5000) return false;
    }
    else return false;
    return true;
}

const url_send_message = '/api/message/'

function sendContactMessage(e)
{
    e.preventDefault();
    if (!checkContactForm()) { showModal('Error!', 'Invalid Form Values'); return; }

    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_send_message, 
        method: "POST",
        data: {
            name: contactName.value,
            email: contactEmail.value,
            subject: contactSubject.value,
            message: contactMessage.value,
        },
        success: function(data){
            if (data['sent'])
            {
                if (contactName) contactName.value = "";    
                if (contactEmail) contactEmail.value = "";
                if (contactSubject) contactSubject.value = "";
                if (contactMessage) contactMessage.value = "";
                showModal('Success', 'We have received your message, and will be getting back to you shortly.');
            }
            else
            {
                showModal('Error!', `Failed to send message:<br/>${data['message']}`);
            }
        },
        error: function(error){
            showModal('Error!', `An unknown error has occured<br/> Please try again later`);
        }
    });
}