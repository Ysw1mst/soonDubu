document.addEventListener('DOMContentLoaded', () => {
    const separators = document.querySelectorAll('.separator');
    let isResizing = false;
    let currentBox = null;
    let nextBox = null;
    let startX = 0;
    let startWidth = 0;
    let nextStartWidth = 0;

    separators.forEach(separator => {
        separator.addEventListener('mousedown', (e) => {
            isResizing = true;
            currentBox = separator.previousElementSibling;
            nextBox = separator.nextElementSibling;
            startX = e.clientX;
            startWidth = currentBox.getBoundingClientRect().width;
            nextStartWidth = nextBox.getBoundingClientRect().width;
            document.body.style.cursor = 'col-resize';
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (isResizing) {
                const dx = e.clientX - startX;
                currentBox.style.flex = `0 0 ${startWidth + dx}px`;
                nextBox.style.flex = `0 0 ${nextStartWidth - dx}px`;
            }
        });

        document.addEventListener('mouseup', () => {
            if (isResizing) {
                isResizing = false;
                document.body.style.cursor = 'default';
            }
        });
    });
});