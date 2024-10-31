const resizers = document.querySelectorAll('.resizer');
let isResizing = false;

resizers.forEach(resizer => {
    resizer.addEventListener('mousedown', function (e) {
        isResizing = true;
        document.addEventListener('mousemove', resizeBoxes);
        document.addEventListener('mouseup', stopResizing);
    });
});

function resizeBoxes(e) {
    if (!isResizing) return;

    const containerWidth = document.querySelector('.container').clientWidth;
    const leftBox = document.querySelector('.left-box');
    const middleBox = document.querySelector('.middle-box');
    const rightBox = document.querySelector('.right-box');

    let newLeftWidth = e.clientX - leftBox.offsetLeft;
    let newRightWidth = containerWidth - newLeftWidth - middleBox.offsetWidth;

    if (newLeftWidth < 100 || newRightWidth < 100) return;

    leftBox.style.flex = `0 0 ${newLeftWidth}px`;
    middleBox.style.flex = `2`;
    rightBox.style.flex = `0 0 ${newRightWidth}px`;
}

function stopResizing() {
    isResizing = false;
    document.removeEventListener('mousemove', resizeBoxes);
    document.removeEventListener('mouseup', stopResizing);
}