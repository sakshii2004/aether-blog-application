document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const blogId = this.getAttribute('data-id');
            const likeCountElement = this.nextElementSibling;  // Assuming like count is right next to the button
            const button = this;  // Preserve `this` context

            fetch(`/like/${blogId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                // Toggle button text between 'Like' and 'Unlike'
                button.textContent = button.textContent === 'Like' ? 'Unlike' : 'Like';
                // Update the like count
                likeCountElement.textContent = `${data.likes}`;
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    });
});
