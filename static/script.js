const resizers = document.querySelectorAll('.resizer');
const boxes = document.querySelectorAll('.box');

resizers.forEach((resizer, index) => {
    let startX;
    let startWidth;

    resizer.addEventListener('mousedown', (e) => {
        startX = e.clientX;
        startWidth = boxes[index].offsetWidth;

        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    });

    function resize(e) {
        const newWidth = startWidth + (e.clientX - startX);
        if (newWidth > 100 && newWidth < 500) { // 최소 및 최대 너비 제한
            boxes[index].style.width = newWidth + 'px';
        }
    }

    function stopResize() {
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }
});