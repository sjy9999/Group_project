// like.js 
document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); //CSRF token
    const likeButtons = document.querySelectorAll('.like-emoji');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const replyId = this.dataset.replyId; //  data-reply-id  reply ID
            sendLike(replyId, csrfToken);
        });
    });
});

function sendLike(replyId, csrfToken) {
    fetch('/like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrfToken  //  CSRF token 
        },
        body: JSON.stringify({ reply_id: replyId })  // reply_id
    })
    .then(response => {
        if (response.ok) {
            return response.json();  // 200 
        } else if (response.status === 401) {
            alert('You must be logged in to like replies.');  
            window.location.href = '/login';  
            return;
        } else {
            throw new Error('Something went wrong on the server.');  
        }
    })
    .then(data => {
        if (data && data.message === 'Like successful') {
            const likeCountSpan = document.getElementById('like-count-' + replyId);
            likeCountSpan.textContent = data.like_count;  
        } else {
            alert(data.message);  //  "Like successful"
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to process like action.');  
    });
}
