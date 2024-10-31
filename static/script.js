const resizers = document.querySelectorAll('.resizer');
const boxes = document.querySelectorAll('.box');

resizers.forEach((resizer) => {
    let startX;
    let startWidth;
    let targetBox;

    resizer.addEventListener('mousedown', (e) => {
        startX = e.clientX;
        targetBox = resizer.parentElement;
        startWidth = targetBox.offsetWidth;

        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    });

    function resize(e) {
        const offset = e.clientX - startX;
        if (resizer.classList.contains('resizer-left')) {
            const newWidth = startWidth - offset;
            if (newWidth > 100) {
                targetBox.style.width = newWidth + 'px';
            }
        } else if (resizer.classList.contains('resizer-right')) {
            const newWidth = startWidth + offset;
            if (newWidth > 100) {
                targetBox.style.width = newWidth + 'px';
            }
        }
    }

    function stopResize() {
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }
});