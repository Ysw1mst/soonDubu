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

window.addEventListener("DOMContentLoaded", () => {
    const leftBox = document.querySelector(".left-box");
    const middleBox = document.querySelector(".middle-box");
    const rightBox = document.querySelector(".right-box");

    // 중앙 박스를 조절할 때 양쪽 박스도 비율에 맞춰 조정하는 함수
    function adjustBoxes() {
        const containerWidth = middleBox.parentElement.offsetWidth;
        const middleWidth = middleBox.offsetWidth;

        // 1:2:1 비율에 맞추어 left와 right의 너비 계산
        const leftWidth = (containerWidth - middleWidth) / 2;
        leftBox.style.width = `${leftWidth}px`;
        rightBox.style.width = `${leftWidth}px`;
    }

    // 중앙 박스의 크기 변경을 감지
    new ResizeObserver(adjustBoxes).observe(middleBox);

    // 처음 로드 시 조정 실행
    adjustBoxes();
});