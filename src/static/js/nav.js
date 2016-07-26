$(document).ready(function () {
    $('.menu li span').css('opacity', '0');
    $('.menu > ul > li').hover(function () {
        $(this).find('ul').show();
        $(this).find('span:first').stop(true).animate(
    		{
    		    top: -14,
    		    opacity: 100
    		}, 100
    	);
        $(this).addClass('active');
    }, function () {
        $(this).find('ul').hide();
        $(this).find('span:first').stop(true).animate(
    		{
    		    top: 0,
    		    opacity: 0
    		}, 100
    	);
        $(this).removeClass('active');
    });
    $('.menu li li').hover(function () {
        $(this).find('span').stop(true).animate(
			{
			    top: 16,
			    opacity: 100
			}, 100
		);
    }, function () {
        $(this).find('span').stop(true).animate(
			{
			    top: 0,
			    opacity: 0
			}, 100
		);
    });
});

