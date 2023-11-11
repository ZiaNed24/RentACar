// ==================================================
// Project Name  :  ----------
// File          :  JS Base
// Version       :  1.0.0
// Last change   :  -- ----- ----
// Author        :  ----------
// Developer:    :  Rakibul Islam Dewan
// ==================================================


(function($) {
  "use strict";


  // back to top - start
  // --------------------------------------------------
  $(window).scroll(function() {
    if ($(this).scrollTop() > 200) {
      $('.backtotop:hidden').stop(true, true).fadeIn();
    } else {
      $('.backtotop').stop(true, true).fadeOut();
    }
  });
  $(function() {
    $(".scroll").on('click', function() {
      $("html,body").animate({
        scrollTop: $("#thetop").offset().top
      }, "slow");
      return false
    })
  });
  // back to top - end
  // --------------------------------------------------


  // preloader - start
  // --------------------------------------------------
  $(window).on('load', function() {
    $('.preloader').addClass('loaded');
    if ($('.preloader').hasClass('loaded')) {
      $('.spinner').delay(1000).queue(function () {
        $(this).remove();
      });
    }
  });
  // preloader - end
  // --------------------------------------------------


  // background - start
  // --------------------------------------------------
  $("[data-bg-color]").each(function () {
    $(this).css("background-color", $(this).attr("data-bg-color"))
  });

  $("[data-bg-gradient]").each(function () {
    $(this).css("background-image", $(this).attr("data-bg-gradient"))
  });
  
  $('[data-bg-image]').each(function() {
    $(this).css('background-image', 'url('+ $(this).attr('data-bg-image') + ')');
  });
  // background - end
  // --------------------------------------------------


  // background parallax - start
  // --------------------------------------------------
  $(".parallaxie").parallaxie({
    offset: 0,
    speed: 0.3,
  });
  // background parallax - end
  // --------------------------------------------------


  // mouse move parallax - start
  // --------------------------------------------------
  if ($('.scene').length > 0 ) {
    $('.scene').mousemoveparallax({
      scalarX: 10.0,
      scalarY: 10.0,
    }); 
  }
  // mouse move parallax - end
  // --------------------------------------------------


  // scroll animation - start
  // --------------------------------------------------
  AOS.init({
    // disable: function() {
    //   var maxWidth = 769;
    //   return window.innerWidth < maxWidth;
    // }
    once: true,
    duration: 800,
  });
  // scroll animation - end
  // --------------------------------------------------


  // sticky header - start
  // --------------------------------------------------
  $(window).on('scroll', function () {
    if ($(this).scrollTop() > 200) {
      $('.sticky').addClass("stuck")
    } else {
      $('.sticky').removeClass("stuck")
    }
  });
  // sticky header - end
  // --------------------------------------------------


  // mobile sidebar menu - start
  // --------------------------------------------------
  $(document).ready(function () {
    $('.close_btn, .overlay').on('click', function () {
      $('.mobile_sidebar_menu').removeClass('active');
      $('.overlay').removeClass('active');
    });

    $('.mobile_sidebar_btn').on('click', function () {
      $('.mobile_sidebar_menu').addClass('active');
      $('.overlay').addClass('active');
    });
  });
  // mobile sidebar menu - end
  // --------------------------------------------------


  // counter - start
  // --------------------------------------------------
  $('.counter').counterUp({
    delay: 10,
    time: 1000
  });
  // counter - end
  // --------------------------------------------------


})(jQuery);