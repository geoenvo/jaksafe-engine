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
    
    /* Activate sidebar menu once the page is displayed */
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
    
    /* Smooth scrolling sidebar */
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
    
    /* Enable click and drag scrollable page */
    var x,y,top,left,down;
    $("#scrollable").mousedown(function(e){
        e.preventDefault();
        down=true;
        x=e.pageX;
        y=e.pageY;
        top=$(this).scrollTop();
        left=$(this).scrollLeft();
    });
    $("body").mousemove(function(e){
        if(down){
            var newX=e.pageX;
            var newY=e.pageY;
            
            //console.log(y+", "+newY+", "+top+", "+(top+(newY-y)));
            
            $("#scrollable").scrollTop(top-newY+y);    
            $("#scrollable").scrollLeft(left-newX+x);    
        }
    });
    $("body").mouseup(function(e){down=false;});
});