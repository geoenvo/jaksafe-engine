$(document).ready(function() {
    /* Date picker */
    if ($('#filter .datepicker').length > 0) {
        $('#filter #t0').datetimepicker({
            format: 'YYYY-MM-DD',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
        $('#filter #t1').datetimepicker({
            format: 'YYYY-MM-DD',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
    }
    
    /* Date & time picker */
    if ($('#filter .datetimepicker').length > 0) {
        $('#filter #t0').datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
        $('#filter #t1').datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
    }
      
    /* Smooth scrolling sidebar: Activate sidebar as the menu is clicked */
    $('a[href*=#]:not([href=#])').click(function() {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
            $('html,body').animate({
                scrollTop: target.offset().top
            }, 1000);
            return false;
        }
    });
    
    /* Activate sidebar once the page is displayed */
    $(window).on('scroll', function () {
        var scrollPos = $(document).scrollTop();
        $('.sidebar-menu a').each(function () {
            var currLink = $(this);
            var refElement = $(currLink.attr("href"));
            if (refElement.position().top <= scrollPos && refElement.position().top + refElement.height() > scrollPos) {
                $(".sidebar-menu a").find(".active").removeClass("active");
                currLink.addClass("active");
            }
            else{
                currLink.removeClass("active");
            }
        });
    });
    
    /* Manage sidebar position as the page is scrolled */
    if ( ($(window).height() + 100) < $(document).height() ) {
        $('#sidebar-block').affix({
            offset: {top:100}
        });
    }
    
    /* Manage "back to top" position as the page is scrolled */
    if ( ($(window).height() + 100) < $(document).height() ) {
        $('#top-link-block').removeClass('hidden').affix({
            offset: {top:100}
        });
    }
});