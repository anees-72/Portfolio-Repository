document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            this.style.display = "none";
            const saveBtn = document.getElementById(`save-${postId}`);
            saveBtn.style.display = "inline-block";
            const cancelBtn = document.getElementById(`cancel-${postId}`);
            cancelBtn.style.display = "inline-block";
            document.getElementById(`content-${postId}`).style.display = "none";
            document.getElementById(`textarea-${postId}`).style.display = "block";
            cancelBtn.addEventListener('click', function() {
                document.getElementById(`content-${postId}`).style.display = "block";
                document.getElementById(`textarea-${postId}`).style.display = "none";
                this.style.display = "none";
                saveBtn.style.display = "none";
                button.style.display = "inline-block";
            });
            saveBtn.addEventListener('click', function() {
                const newContent = document.getElementById(`textarea-${postId}`).value;

                fetch('/edit_post', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({
                        post_id: postId,
                        content: newContent
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById(`content-${postId}`).innerText = newContent;
                        document.getElementById(`content-${postId}`).style.display = "block";
                        document.getElementById(`textarea-${postId}`).style.display = "none";
                        saveBtn.style.display = "none";
                        cancelBtn.style.display = "none";
                        button.style.display = "inline-block";
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        });
    });
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');

            fetch('/toggle_like', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const likeCount = document.getElementById(`like-count-${postId}`);
                    likeCount.innerText = data.likes_count;
                    const likeIcon = this.querySelector('i');
                    likeIcon.classList.toggle('bi-heart-fill');
                    likeIcon.classList.toggle('bi-heart');
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
