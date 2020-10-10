// ####################################
//
// csrf cookie
//
// ####################################

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var csrftoken = getCookie('csrftoken');

var headers = new Headers();
headers.append('X-CSRFToken', csrftoken);

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// ####################################
//
// modals api
//
// ####################################

var mainAppModalCloseAction = null;
var scrollLargeModalCloseAction = null;

function showModal(title, content) {
    $('#mainAppModalTitle').html(title)
    $('#mainAppModalContent').html(content)
    $('#mainAppModal').modal('show')
}

function showModalAction(title, content, closeAction) {
    $('#mainAppModalTitle').html(title)
    $('#mainAppModalContent').html(content)
    $('#mainAppModal').modal('show')
    mainAppModalCloseAction = closeAction;
}

$('#mainAppModal').on('hidden.bs.modal', function (e) {
    $('#mainAppModalTitle').html('Modal title')
    $('#mainAppModalContent').html('...')
    if (mainAppModalCloseAction) mainAppModalCloseAction();
    mainAppModalCloseAction = null;
})


function showScrollLargeModal(title, content) {
    $('#scrollLargeModalTitle').html(title)
    $('#scrollLargeModalContent').html(content)
    $('#scrollLargeModal').modal('show')
}

function showScrollLargeModalAction(title, content, closeAction) {
    console.log("here")
    $('#scrollLargeModalTitle').html(title)
    $('#scrollLargeModalContent').html(content)
    $('#scrollLargeModal').modal('show')
    scrollLargeModalCloseAction = closeAction;
}

$('#scrollLargeModal').on('hidden.bs.modal', function (e) {
    $('#scrollLargeModalTitle').html('Modal title')
    $('#scrollLargeModalContent').html('...')
    if (scrollLargeModalCloseAction) scrollLargeModalCloseAction();
    scrollLargeModalCloseAction = null;
})

function showConfirmationModal(title, content, confirmAction) {
    if (title) $('#confirmationModalTitle').html(title)
    $('#confirmationModalContent').html(content)
    $('#confirmationModalConfirm').on('click.confirmAction', () => {
        confirmAction();
        $('#confirmationModal').modal('hide');
    })
    $('#confirmationModal').modal('show')
}

function showConfirmationModalCustom(title, content, customText, confirmAction) {
    $('#confirmationModalConfirm').html(customText)
    showConfirmationModal(title, content, confirmAction)
}

$('#confirmationModal').on('hidden.bs.modal', function (e) {
    $('#confirmationModalConfirm').html("Yes, I'm sure")
    $('#confirmationModalConfirm').off('click.confirmAction')
    $('#confirmationModalTitle').html('Confirmation')
    $('#confirmationModalContent').html('...')
})

// ####################################
//
// newsletter api
//
// ####################################

const newsletterEmail = document.getElementById('newsletter-email')
function checkNewsletterForm() 
{
    if (newsletterEmail) {
        if (newsletterEmail.value.length < 1 || newsletterEmail.value.length > 100) return false;
    }
    else return false;
    return true;
}

const url_subscribe_newsletter = '/api/newsletter/subscribe/'

function subscribeNewsletter(e)
{
    e.preventDefault();
    if (!checkNewsletterForm()) { showModal('Error!', 'Invalid email'); return; }
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_subscribe_newsletter, 
        method: "POST",
        data: {
            email: newsletterEmail.value,
        },
        success: function(data){
            if (data['added'])
            {
                if (newsletterEmail) newsletterEmail.value = "";
                showModal('Congratulations', 'You are now subscribed to our Newsletter!');
            }
            else
            {
                showModal('Error!', `Failed to subscribe:<br/>${data['message']}`);
            }
        },
        error: function(error){
            showModal('Error!', `An unknown error has occured<br/> Please try again later`);
        }
    });
}