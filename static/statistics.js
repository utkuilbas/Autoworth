 document.addEventListener('DOMContentLoaded', function () {
            const modal = document.getElementById('modal');
            const modalImg = document.getElementById('modal-img');
            const closeBtn = document.getElementById('close');

            document.querySelectorAll('.stat-image').forEach(image => {
                image.addEventListener('click', function () {
                    modal.style.display = 'flex';
                    modalImg.src = this.src;
                });
            });

            closeBtn.addEventListener('click', () => modal.style.display = 'none');
            modal.addEventListener('click', () => modal.style.display = 'none');
        });