document.getElementById("resetButton").addEventListener("click", function() {
    // 파일 선택 초기화
    document.querySelector('input[type="file"]').value = ""; 
    // 변환된 MIDI 파일 다운로드 링크 초기화
    const downloadLink = document.querySelector('a[href*="static"]');
    if (downloadLink) {
        downloadLink.parentNode.removeChild(downloadLink); // 링크 제거
    }
    // 업로드 상태 초기화 메시지 추가
    alert("초기화되었습니다.");
});

// 구분선 조정 기능 추가
const dividers = document.querySelectorAll('.divider');
dividers.forEach(divider => {
    divider.addEventListener('mousedown', initResize);
});

function initResize(e) {
    window.addEventListener('mousemove', Resize);
    window.addEventListener('mouseup', stopResize);
}

function Resize(e) {
    const leftBox = e.target.previousElementSibling;
    const rightBox = e.target.nextElementSibling;

    if (leftBox && rightBox) {
        leftBox.style.width = `${e.clientX}px`;
        rightBox.style.width = `${window.innerWidth - e.clientX - 20}px`; // 20px는 여백
    }
}

function stopResize() {
    window.removeEventListener('mousemove', Resize);
    window.removeEventListener('mouseup', stopResize);
}