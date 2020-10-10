// ####################################
//
// comments and replies
//
// ####################################

document.getElementById('post-comment-button').addEventListener('click', createComment)

var nameInput = document.getElementById('post-comment-name')
var emailInput = document.getElementById('post-comment-email')
var websiteInput = document.getElementById('post-comment-website')
var contentInput = document.getElementById('post-comment-content')

var commentList = document.getElementById('blog-comment-list')

function checkCommentForm() 
{
    if (contentInput)
    {
        if (contentInput.value.length < 1 || contentInput.value.length > 500) return false;
    }
    else return false;

    if (nameInput)
    {
        if (nameInput.value.length < 1 || nameInput.value.length > 50) return false;
    }

    if (emailInput)
    {
        if (emailInput.value.length < 1 || emailInput.value.length > 50) return false;
    }

    if (websiteInput)
    {
        if (websiteInput.value.length > 50) return false;
    }

    return true;
}

function createComment(e)
{
    e.preventDefault()
    data = {}
    if (!checkCommentForm()) { showModal('Error!', 'Invalid Form Values'); return; }
    if (user_is_authenticated)
    {
        data = {
            'blog_id': blog_id,
            'content': contentInput.value,
        }
    }
    else 
    {
        data = {
            'blog_id': blog_id,
            'name': nameInput.value,
            'email': emailInput.value,
            'website': websiteInput.value,
            'content': contentInput.value,
        }
    }
    postComment_AJAX(data);
}

const url_comment_create = '/api/comments/create/'
const url_comment_delete = '/api/comments/delete/'
const url_reply_create = '/api/replies/create/'
const url_reply_delete = '/api/replies/delete/'

function postComment_AJAX(post_data) 
{
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_comment_create, 
        method: "POST",
        data: post_data,
        success: function(data){
            handler_createComment(data);
        },
        error: function(error){
            handler_error(error);
        }
    });
}

function handler_createComment(data)
{
    if (data['added'])
    {
        if (contentInput) contentInput.value = "";    
        if (nameInput) nameInput.value = "";
        if (emailInput) emailInput.value = "";
        if (websiteInput) websiteInput.value = "";
        if (data['comment_html']) commentList.innerHTML += data['comment_html']
        showModal('Success', 'Your comment has been succesfully added');
    }
    else
    {
        showModal('Error!', `Failed to add comment:<br/>${data['message']}`);
    }
}

function toggleReplyForm(id)
{
    const formSpan = document.getElementById(`reply-form-${id}`);
    const replyButton = document.getElementById(`reply-button-${id}`);

    if (formSpan.innerHTML === "")
    {
        replyButton.innerText='CANCEL';
        replyButton.style.background='#ff4838';
        replyButton.style.color='white';

        if (user_is_authenticated)
        {
            formSpan.innerHTML = `    
            <div class="comment-form-wrap">
                <form class="pl-4 bg-light">
                    <div class="form-group">
                        <label for="post-reply-content-${id}">Reply Message</label>
                        <textarea maxlength="500" name="" cols="30" rows="6" class="form-control" id="post-reply-content-${id}"></textarea>
                    </div>
                    <div class="form-group">
                        <input value="Submit Reply" type="submit" class="btn py-3 px-4 btn-primary" id="post-reply-button" onclick="createReply(event, ${id})">
                    </div>
                </form>
            </div>`
        }
        else
        {
            formSpan.innerHTML = `    
            <div class="comment-form-wrap">
                <form class="pl-4 bg-light">
                    <div class="form-group">
                        <label for="post-reply-name-${id}">Name *</label>
                        <input maxlength="50" type="text" class="form-control" id="post-reply-name-${id}">
                    </div>
                    <div class="form-group">
                        <label for="post-reply-content-${id}">Reply Message</label>
                        <textarea maxlength="500" name="" id="post-reply-content-${id}" cols="30" rows="6" class="form-control"></textarea>
                    </div>
                    <div class="form-group">
                        <input type="submit" value="Submit Reply" class="btn py-3 px-4 btn-primary" id="post-reply-button" onclick="createReply(event, ${id})">
                    </div>
                </form>
            </div>`
        }
        document.getElementById(`post-reply-content-${id}`).focus();
    }
    else
    {
        replyButton.innerText = 'REPLY';
        replyButton.style = "cursor: pointer;";
        formSpan.innerHTML = "";
    }

}

function checkReplyForm(contentInput, nameInput) 
{
    if (contentInput)
    {
        if (contentInput.value.length < 1 || contentInput.value.length > 500) return false;
    }
    else return false;

    if (nameInput)
    {
        if (nameInput.value.length < 1 || nameInput.value.length > 50) return false;
    }

    return true;
}

function createReply(e, id)
{
    e.preventDefault()
    data = {}
    const contentInput = document.getElementById(`post-reply-content-${id}`)
    const nameInput = document.getElementById(`post-reply-name-${id}`)
    if (!checkReplyForm(contentInput, nameInput)) { showModal('Error!', 'Invalid Form Values'); return; }
    if (user_is_authenticated)
    {
        data = {
            'comment_id': id,
            'content': contentInput.value,
        }
    }
    else 
    {
        data = {
            'comment_id': id,
            'name': nameInput.value,
            'content': contentInput.value,
        }
    }
    postReply_AJAX(data, id);
}

function postReply_AJAX(post_data, id) 
{
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }, 
        url: url_reply_create, 
        method: "POST",
        data: post_data,
        success: function(data){
            handler_createReply(data, id);
        },
        error: function(error){
            handler_error(error);
        }

    });
}

function handler_createReply(data, id)
{
    if (data['added'])
    {
        toggleReplyForm(id);
        const replyList = document.getElementById(`comment-reply-list-${id}`)
        if (!replyList)
        {
            const commentBody = document.getElementById(`comment-body-${id}`)
            commentBody.innerHTML += `
                <ul class="children pt-3" id="comment-reply-list-${id}">
                </ul>`
            const newReplyList = document.getElementById(`comment-reply-list-${id}`)
            if (data['reply_html']) newReplyList.innerHTML += data['reply_html']
        }
        else if (data['reply_html']) replyList.innerHTML += data['reply_html']
        showModal('Success', 'Your reply has been succesfully added');
    }
    else
    {
        showModal('Error!', `Failed to add reply:<br/>${data['message']}`);
    }
}

function deleteComment(id)
{
    showConfirmationModal(null, 'Are you sure you want to delete this comment (and all its replies) ?', () => {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }, 
            url: url_comment_delete, 
            method: "POST",
            data: {
                'comment_id': id,
            },
            success: function(data){
                handler_deleteComment(data, id);
            },
            error: function(error){
                handler_error(error);
            }
    
        });
    })
}

function handler_deleteComment(data, id)
{
    if (data['deleted'])
    {
        showModal('Success', 'Comment deleted');
        const commentBody = document.getElementById(`comment-body-${id}`)
        if (commentBody) commentBody.remove()
    }
    else
    {
        showModal('Error!', `Failed to delete comment:<br/>${data['message']}`);
    }
}


function deleteReply(id)
{
    showConfirmationModal(null, 'Are you sure you want to delete this reply ?', () => {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }, 
            url: url_reply_delete, 
            method: "POST",
            data: {
                'reply_id': id,
            },
            success: function(data){
                handler_deleteReply(data, id);
            },
            error: function(error){
                handler_error(error);
            }
    
        });
    })
}

function handler_deleteReply(data, id)
{
    if (data['deleted'])
    {
        showModal('Success', 'Reply deleted');
        const replyBody = document.getElementById(`reply-body-${id}`)
        if (replyBody) replyBody.remove()
    }
    else
    {
        showModal('Error!', `Failed to delete reply:<br/>${data['message']}`);
    }
}

function handler_error(error)
{
    showModal('Error!', `An unknown error has occured`);
}

