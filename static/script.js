const separators = document.querySelectorAll('.separator');
const leftBox = document.querySelector('.left-box');
const middleBox = document.querySelector('.middle-box');
const rightBox = document.querySelector('.right-box');

separators.forEach(separator => {
    separator.addEventListener('mousedown', function (e) {
        e.preventDefault();

        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    });

    function resize(e) {
        const containerWidth = document.querySelector('.container').offsetWidth;

        if (separator.previousElementSibling === leftBox) {
            let newWidth = e.clientX - leftBox.getBoundingClientRect().left;
            leftBox.style.flex = `0 0 ${Math.max(newWidth, containerWidth * 0.1)}px`;
            middleBox.style.flex = `0 0 ${Math.max(containerWidth - newWidth - rightBox.offsetWidth, containerWidth * 0.2)}px`;
        } else if (separator.previousElementSibling === middleBox) {
            let newWidth = e.clientX - middleBox.getBoundingClientRect().left;
            middleBox.style.flex = `0 0 ${Math.max(newWidth, containerWidth * 0.2)}px`;
            rightBox.style.flex = `0 0 ${Math.max(containerWidth - newWidth - leftBox.offsetWidth, containerWidth * 0.1)}px`;
        }
    }

    function stopResize() {
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }
});