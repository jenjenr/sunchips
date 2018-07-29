$(function() {


    $('#home').parallax('50%', 0.4);

    $('.pattern-overlay').parallax('20%', 0.6);
    
    $('.slider').bxSlider({
        auto: true,
        stopAutoOnClick: true,
        autoStart: true,
        infiniteLoop: false,
        captions: true,
        touchEnabled: true,
        pager: false,
        hideControlOnEnd: true,
        nextText: 'USDA afer re-Design',
        beforeText: 'USDA site design'
    });


});

function closeMobileNav() {
    var x = document.getElementById("HamburgerToggle").getAttribute("aria-expanded"); 
    if (x == "true") 
    {
        $('.navbar-toggle').click();
    } else {
        // do nothing
    }
}



function myFunction() {

    
}