// like.js 文件内容
document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // 获取 CSRF token
    const likeButtons = document.querySelectorAll('.like-emoji');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const replyId = this.dataset.replyId; // 从 data-reply-id 获取 reply ID
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
            'X-CSRFToken': csrfToken  // 添加 CSRF token 到请求头中
        },
        body: JSON.stringify({ reply_id: replyId })  // 发送 reply_id
    })
    .then(response => {
        if (response.ok) {
            return response.json();  // 解析 JSON 仅当响应状态码为 200 时
        } else if (response.status === 401) {
            alert('You must be logged in to like replies.');  // 处理未登录状态
            window.location.href = '/login';  // 可以选择重定向到登录页面
            return;
        } else {
            throw new Error('Something went wrong on the server.');  // 抛出其他错误
        }
    })
    .then(data => {
        if (data && data.message === 'Like successful') {
            const likeCountSpan = document.getElementById('like-count-' + replyId);
            likeCountSpan.textContent = data.like_count;  // 使用后端返回的最新点赞数更新前端显示
        } else {
            alert(data.message);  // 如果返回的消息不是 "Like successful"，显示错误消息
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to process like action.');  // 提供给用户的信息可以更友好
    });
}
