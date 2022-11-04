
//랜덤 음식
const row = document.querySelector("#random-food");
var foodsList = ["떡볶이.jpg", "삼겹살.jpg", "치킨.png", "피자.jpg", "김밥.jpg", '비빔밥.jpg', '죽.jpg', '칼국수.jpg', '물냉면.jpg', '짜장면.jpg', '짬뽕.jpg', '떡갈비.jpg', '갈비찜.jpg', '해물찜.jpg', '계란말이.jpg', '순대국.jpg', '감자탕.jpg',];
temp(0);

function temp(num) {
    var template = [];
    for (let i = 0; i < 4; i++) {
        var a = foodsList[(i + num) % foodsList.length];
        var url = "{% static 'restaurants/img/change' %}".replace("change", a);
        template.push(`<div class="col text-center"><img src="${url}" alt="" class="img-fluid rounded-pill"></div>`);
        row.insertAdjacentHTML("beforeend", template[i]);
    }
}

const shuffleMenu = document.querySelector("#shuffle-menu");
shuffleMenu.addEventListener("click", () => {
    row.innerHTML = "";
    temp(Math.floor(Math.random() * (foodsList.length - 1 - 0) + 1));
});

// 캐러셀
document.querySelector('.slide-2').addEventListener('click', () => {
    document.querySelector('.slide-container').style.transform = 'translateX(-100vw)'
    document.querySelector('.slide-2').classList.add('active')
    document.querySelector('.slide-1').classList.remove('active')
    document.querySelector('.slide-3').classList.remove('active')
})
document.querySelector('.slide-3').addEventListener('click', () => {
    document.querySelector('.slide-container').style.transform = 'translateX(-200vw)'
    document.querySelector('.slide-3').classList.add('active')
    document.querySelector('.slide-1').classList.remove('active')
    document.querySelector('.slide-2').classList.remove('active')
})
document.querySelector('.slide-1').addEventListener('click', () => {
    document.querySelector('.slide-container').style.transform = 'translateX(0vw)'
    document.querySelector('.slide-1').classList.add('active')
    document.querySelector('.slide-2').classList.remove('active')
    document.querySelector('.slide-3').classList.remove('active')
})

//    인기검색어 클릭
const populars = document.querySelectorAll('.e1387oiq0');
populars.forEach((el) => {
    el.addEventListener('click', (e) => {
        document.querySelector('#search').value = e.currentTarget.innerText
    })
})

// 캐러셀 실패
/* {% comment %}
  <script>
    var start = 0
    var clicking = false
    var slideBox = document.querySelectorAll('.slide-box')

    SlideBox(0)
    SlideBox(1)
    SlideBox(2)

    function SlideBox(num) {
      SlideBoxMouseDown(num)
      SlideBoxMouseMove(num)
      SlideBoxMouseUp(num)
    }

    function SlideBoxMouseDown(num) {
      slideBox[num].addEventListener('mousedown', (e) => {
        start = e.screenX
        clicking = true
      })
    }
    function SlideBoxMouseMove(num) {
      slideBox[num].addEventListener('mousemove', (e) => {
        if (clicking == true) {
          document.querySelector('.slide-container').style.transform = `translateX(${(-1) * (num * 100) + e.screenX - start}px)`
        }
      })
    }
    function SlideBoxMouseUp(num) {
      slideBox[num].addEventListener('mouseup', (e) => {
        clicking = false
        if (e.clientX - start < -100) {
          document.querySelector('.slide-container').style.transform = `translateX(-${((num + 1) * 100) % 300}vw)`
          document.querySelector('.slide-container').style.transition = 'all 0.5s'
        } else {
          document.querySelector('.slide-container').style.transform = `translateX(-${(num * 100) % 300}vw)`
          document.querySelector('.slide-container').style.transition = 'all 0.5s'
        }
        setTimeout(() => {
          document.querySelector('.slide-container').style.transition = 'none'
        }, 500)
      })
    }
    
  </scrip > {% endcomment %} */