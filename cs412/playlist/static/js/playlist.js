document.addEventListener("DOMContentLoaded", function () {
    // 1. Clickable song rows
    const songRows = document.querySelectorAll(".song-row");

    songRows.forEach((row) => {
        row.addEventListener("mouseover", function () {
            row.style.backgroundColor = "#f0f0f0";
            row.style.cursor = "pointer";
        });

        row.addEventListener("mouseout", function () {
            row.style.backgroundColor = "";
        });

        row.addEventListener("click", function () {
            const link = row.querySelector("a");
            if (link) {
                window.location.href = link.href;
            }
        });
    });

    // 2. Album slideshow logic (for artist detail page)
    const slides = document.querySelectorAll(".album-slide");
    let slideIndex = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.display = i === index ? "block" : "none";
        });
    }

    function nextSlide() {
        slideIndex = (slideIndex + 1) % slides.length;
        showSlide(slideIndex);
    }

    if (slides.length > 0) {
        showSlide(slideIndex);
        setInterval(nextSlide, 3000); // switch slide every 3 seconds
    }
});
