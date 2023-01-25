/* The initial version is taken from
https://github.com/pytorch/pytorch_sphinx_theme
under MIT license
*/
window.mobileMenu = {
    bind: function () {
        $("[data-behavior='open-mobile-menu']").on('click', function (e) {
            e.preventDefault();
            $(".mobile-main-menu").addClass("open");
            $("body").addClass('no-scroll');

            mobileMenu.listenForResize();
        });

        $("[data-behavior='close-mobile-menu']").on('click', function (e) {
            e.preventDefault();
            mobileMenu.close();
        });
    },

    listenForResize: function () {
        $(window).on('resize.ForMobileMenu', function () {
            if ($(this).width() > 768) {
                mobileMenu.close();
            }
        });
    },

    close: function () {
        $(".mobile-main-menu").removeClass("open");
        $("body").removeClass('no-scroll');
        $(window).off('resize.ForMobileMenu');
    }
};
$(document).ready(function () {
    mobileMenu.bind();
});
