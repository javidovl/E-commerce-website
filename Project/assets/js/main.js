(function ($) {
 "use strict";
	// jQuery MeanMenu
	jQuery('nav#dropdown').meanmenu();
	//menu a active jquery
	var pgurl = window.location.href.substr(window.location.href
		.lastIndexOf("/")+1);
		$("ul li a").each(function(){
		if($(this).attr("href") == pgurl || $(this).attr("href") == '' )
		$(this).addClass("active");
	$('header ul li ul li a.active').parent('li').addClass('parent-li');
	$('header ul li ul li.parent-li').parent('ul').addClass('parent-ul');
	$('header ul li ul.parent-ul').parent('li').addClass('parent-active');
	})
	//search bar exprnd
	$('.header-top-two .right button').on('click',function(){
		$('.header-top-two .right').toggleClass('widthfull');
	});
	//search bar border color
	$('.middel-top .center').on('click',function(){
		$('.middel-top .center').toggleClass('bordercolor');
	});
	//color select jquery
	$('.color-select > span').on('click',function(){
		$('.color-select > span').toggleClass('outline');
        $(this).addClass("outline").siblings().removeClass("outline");
	});
/*----------------------------
 nivoSlider active
------------------------------ */
	$('#mainSlider').nivoSlider({
		directionNav: true,
		animSpeed: 500,
		effect: 'random',
		slices: 18,
		pauseTime: 10000,
		pauseOnHover: false,
		controlNav: true,
		prevText: '<i class="mdi mdi-chevron-left"></i>',
		nextText: '<i class="mdi mdi-chevron-right"></i>'
	});
/*----------------------------
 plus-minus-button
------------------------------ */
	$(".qtybutton").on("click", function() {
		var $button = $(this);
		var oldValue = $button.parent().find("input").val();
		if ($button.text() == "+") {
			var newVal = parseFloat(oldValue) + 1;
		} else {
			// Don't allow decrementing below zero
			if (oldValue > 0) {
				var newVal = parseFloat(oldValue) - 1;
			} else {
				newVal = 0;
			}
		}
		$button.parent().find("input").val(newVal);
	});
/*----------------------------
 price-slider active
------------------------------ */


function aldas() {
    document.querySelector("#list").children[0].innerHTML = ""
    for (let i = 0; i < filter.getItems().length; i++) {
        $("#list").children(".col-xs-12").append(`<div class="single-list-view">
        <div class="row">
            <div class="col-xs-12 col-md-4">
                <div class="list-img">
                    <div class="product-img">
                        <div class="pro-type sell">
                            <span>sell</span>
                        </div>
                        <a href="${location.origin}/product/${filter._items[i].product}"><img src="${filter._items[i].image_url}" alt="Product Title" /></a>
                    </div>
                </div>
            </div>
            <div class="col-xs-12 col-md-8">
                <div class="list-text">
                    <h3>${filter._items[i].name}</h3>
                    <span>${filter._items[i].category_name}</span>
                    <div class="ratting floatright">
					<p>(${filter._items[i].review_count} Reviews )</p>
                    </div>
                    <h5>$${filter._items[i].price}</h5>
                    <p>${filter._items[i].description.substring(0, 120)}</p>
                    
                </div>
            </div>
        </div>
    </div>`)
    }
}

	$( "#slider-range" ).slider({
		range: true,
		min: 40,
		max: 600,
		values: [ 150, 399 ],
		slide: function( event, ui ) {
		$( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
		},
		change: function(event, ui){
			// console.log(ui.values[0])
			// console.log(ui.values[1])
			filter.getData(`min_price=${ui.values[0]}&max_price=${ui.values[1]}`)
			setTimeout(aldas, 100)
		}
	});
	$( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
	" - $" + $( "#slider-range" ).slider( "values", 1 ) );
/*--------------------------
 scrollUp
---------------------------- */	
	$.scrollUp({
        scrollText: '<i class="mdi mdi-chevron-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });
/*--------------------------
 // simpleLens
 ---------------------------- */
	$('.simpleLens-image').simpleLens({
		
	});
	
})(jQuery); 