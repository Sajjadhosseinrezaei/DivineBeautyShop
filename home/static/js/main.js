// sm(mobile) now
/*const smNav = document.querySelector('.snav');
const closeBtn = document.querySelector('.snav__close-btn');
const closeBtnIcn = document.querySelector('.snav__close-btn-icon');

const navOpenedClass = 'right-0';
const navClosedClass = '-right-[300px]';
const arrowRightClass = 'ri-menu-4-line';
const arrowLeftClass = 'ri-close-large-line';

closeBtn.addEventListener('click', () => {
    if (smNav.classList.contains(navClosedClass)) {
        smNav.classList.toggle(navOpenedClass);

        closeBtnIcn.classList.toggle(arrowRightClass);
        closeBtnIcn.classList.toggle(arrowLeftClass);
    }
})*/

const smNav = document.querySelector('.snav');
const closeBtn = document.querySelector('.snav__close-btn');
const closeBtnIcn = document.querySelector('.snav__close-btn-icon');

const navOpenedClass = 'right-0';
const navClosedClass = '-right-[300px]';
const arrowRightClass = 'ri-menu-4-line';
const arrowLeftClass = 'ri-close-large-line';

closeBtn.addEventListener('click', () => {
    if (smNav.classList.contains(navClosedClass)) {
        smNav.classList.remove(navClosedClass);
        smNav.classList.add(navOpenedClass);
    } else {
        smNav.classList.remove(navOpenedClass);
        smNav.classList.add(navClosedClass);
    }

    closeBtnIcn.classList.toggle(arrowRightClass);
    closeBtnIcn.classList.toggle(arrowLeftClass);
});


/*--------- Scroll Reveal Animations -----------*/

const sr = ScrollReveal({
    origin: 'bottom',
    distance: '60px',
    duration: 3000,
    delay: 600,
    //reset: true,
});
//hero

sr.reveal('.hero__text', { origin: 'top' });

//menu

sr.reveal('.menu__card', { interval: 100, origin: 'top' });
sr.reveal('.menu__card-1', { interval: 100, origin: 'top' });
// main pics
//1

sr.reveal('.main__img_2', { origin: 'right' });
sr.reveal('.main__img_1', { origin: 'left' });

// title
sr.reveal('.about__title', { origin: 'top' });
sr.reveal('.about__title_1', { delay: 800, origin: 'top' });

// popular

sr.reveal('.popular__slider_all', { origin: 'top' });
sr.reveal('.popular__slider', { delay: 800, origin: 'top' });


// footer
sr.reveal('.footer__all', { origin: 'top' })
sr.reveal('.footer__text', { origin: 'top' })
sr.reveal('.footer__floral', { origin: 'left', delay: 800 })
// copy_right

sr.reveal('.copy__right', { origin: 'top' });


/*--------- SWIPER -----------*/
const swiper = new Swiper('.swiper', {
    // Optional parameters
    speed: 400,
    spaceBetween: 30,
    autoplay: {
        delay: 3000,
        disableOnIntraction: false
    },


    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
        clickable: true
    },
    grabCursor: true,
    breakpoints: {
        640: {
            slidesPerView: 1
        },
        768: {
            slidesPerView: 2
        },
        1024: {
            slidesPerView: 3
        },
    }
});


//////// login - code - ///////////
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("myInput");

    if (!input) return; // اگه این input وجود نداره (توی این صفحه)، هیچ کاری نکن

    input.addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, "").slice(0, 4);
    });
});


//////////////////////////////////


document.getElementById("myButton").addEventListener("click", function () {
    window.location.href = "./sign in/signin.html"; // آدرس صفحه بعد
});