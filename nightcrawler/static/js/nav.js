var path = window.location.pathname.split("/");
var path_one = "/"+path[1]+"/";
var path_two = path_one+path[2]+"/";


/*header*/
$(function header(){
	$(".header-right a").each(function(){
		if($(this).attr("href") == path_one || $(this).attr("href") == window.location.pathname){
			$(this).addClass('active');
		}
	});
});

/*news menu*/
$(function menu_news(){
	$(".menu-news a").each(function(){
		if($(this).attr("href") == path_two || $(this).attr("href") == window.location.pathname){
			$(this).addClass('active');
		}
	});
});

$(function menu_dates(){
	$(".menu-dates a").each(function(){
		if($(this).attr("href") == window.location.pathname){
			$(this).addClass('active');
		}
	});
});
