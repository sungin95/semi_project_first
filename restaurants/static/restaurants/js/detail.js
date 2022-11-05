// 북마크 비동기
const likeBtn = document.querySelector("#like-btn");
likeBtn.addEventListener("click", function (e) {
    axios({ method: "get", url: `/${e.target.dataset.restaurantId}/like/` }).then((res) => {
        if (res.data.isLiked === true) {
            e.target.classList.add("bi-star-fill");
            e.target.classList.remove("bi-star");
        } else {
            e.target.classList.add("bi-star");
            e.target.classList.remove("bi-star-fill");
        }
        const likeCount = document.querySelector("#like-count");
        likeCount.innerText = res.data.likeCount;
    });
});

// 캐러셀
var slides = document.querySelector(".slides");
var slide = document.querySelectorAll(".slides li");
var currentIdx = 0;
var slideCount = slide.length;
var preBtn = document.querySelector(".prev");
var nextBtn = document.querySelector(".next");
var slideWidth = 300;
var slideMargin = 30;
var calc = (slideWidth + slideMargin) * slideCount - slideMargin;
slides.style.width = `${calc}px`;

function moveSlide(num) {
    slides.style.left = `${-1 * (num * 330)}px`;
    console.log(-1 * (num * 330));
    currentIdx = num;
}

nextBtn.addEventListener("click", () => {
    if (currentIdx < slideCount - 4) {
        moveSlide(currentIdx + 1);
    } else {
        moveSlide(0);
    }
});
preBtn.addEventListener("click", () => {
    if (currentIdx > 0) {
        moveSlide(currentIdx - 1);
    } else {
        moveSlide(slideCount - 4);
    }
});
