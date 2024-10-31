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