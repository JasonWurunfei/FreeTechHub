(function($) {
  "use strict";
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
      if (this.href === path) {
        $(this).addClass("active");
      }
    });
    $("#sidebarToggle").on("click", function(e) {
      e.preventDefault();
      $("body").toggleClass("sb-sidenav-toggled");
    });
  })(jQuery);
