//<![CDATA[
jQuery( document ).ready( function( $ )
{ 
	$.liveace = {
		init: function()
		{
			function callAfter( currSlideElement, nextSlideElement, options, forwardFlag )
			{
				var activeSlide = jQuery("#slide-menu ul li.activeSlide a").html();
				if (parseInt(activeSlide, 10) == '1')
					jQuery("#slide-menu").css('background-position', '0 0');	

				if (parseInt(activeSlide, 10) == '2')
					jQuery("#slide-menu").css('background-position', '0 -56px');	
				
				if (parseInt(activeSlide, 10) == '3')
					jQuery("#slide-menu").css('background-position', '0 -112px');	
				
				if (parseInt(activeSlide, 10) == '4')
					jQuery("#slide-menu").css('background-position', '0 -168px');

			}
			///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				// homepage cycle slider
				if ( jQuery().cycle ) // check to make sure plugin is loaded first
				{
					jQuery("#homepage-slider").cycle({
						fx:     'fade', 
						speed:  500, 
						pause:	true,
						timeout: 6000,
						slideExpr: '.slide',
						cleartypeNoBg: true,
						sync: true,
						slideResize: false,
						containerResize: false,
						pager: '#slide-menu ul',
						after: callAfter,
						pagerAnchorBuilder: function(idx, slide) { 
							// return selector string for existing anchor 
							return '#slide-menu li:eq(' + idx + ') a'; 
							}
					});
				}
				
				// homepage slider buttons on hover
				var activeSlide;
				jQuery("#slide-menu ul li a").hover(function() 
				{
					var slide = jQuery(this).html();
					//var activeSlide = jQuery("#slide-menu ul li.activeSlide a").html();
					
					if (parseInt(slide, 10) == '1')
						jQuery("#slide-menu").css('background-position', '0 0');	
	
					if (parseInt(slide, 10) == '2')
						jQuery("#slide-menu").css('background-position', '0 -56px');	
					
					if (parseInt(slide, 10) == '3')
						jQuery("#slide-menu").css('background-position', '0 -112px');	
					
					if (parseInt(slide, 10) == '4')
						jQuery("#slide-menu").css('background-position', '0 -168px');
				}, function() 
				{
					activeSlide = jQuery("#slide-menu ul li.activeSlide a").html();
					if (parseInt(activeSlide, 10) == '1')
						jQuery("#slide-menu").css('background-position', '0 0');	
	
					if (parseInt(activeSlide, 10) == '2')
						jQuery("#slide-menu").css('background-position', '0 -56px');	
					
					if (parseInt(activeSlide, 10) == '3')
						jQuery("#slide-menu").css('background-position', '0 -112px');	
					
					if (parseInt(activeSlide, 10) == '4')
						jQuery("#slide-menu").css('background-position', '0 -168px');
					
				});
			///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				// tooltips
				var tip;
				jQuery( ".tooltip" ).hover( function()
				{
			
					//Caching the tooltip and removing it from container; then appending it to the body
					tip = jQuery( this ).find( '.tip' ).remove();
					jQuery( 'body' ).append( tip );
			
					tip.fadeTo( 400, 1 ); //Show tooltip
			
				}, 
				function() 
				{
					tip.hide().remove(); //Hide and remove tooltip appended to the body
					jQuery( this ).append( tip ); //Return the tooltip to its original position
			
				}).mousemove(function(e) {
				//console.log(e.pageX)
					if( typeof(tip) !== "undefined") {
					  var mousex = e.pageX + 20; //Get X coodrinates
					  var mousey = e.pageY + 20; //Get Y coordinates
					  var tipWidth = tip.width(); //Find width of tooltip
					  var tipHeight = tip.height(); //Find height of tooltip
			
					 //Distance of element from the right edge of viewport
					  var tipVisX = jQuery(window).width() - (mousex + tipWidth);
					  var tipVisY = jQuery(window).height() - (mousey + tipHeight);
			
					if ( tipVisX < 20 ) { //If tooltip exceeds the X coordinate of viewport
						mousex = e.pageX - tipWidth - 20;
						jQuery(this).find('.tip').css({  top: mousey, left: mousex });
					} if ( tipVisY < 20 ) { //If tooltip exceeds the Y coordinate of viewport
						mousey = e.pageY - tipHeight - 20;
						tip.css({  top: mousey, left: mousex });
					} else {
						tip.css({  top: mousey, left: mousex });
					}
				  }
				});
			///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				// table sorting
				if ( jQuery().tablesorter ) // check to make sure plugin is loaded first
					$("#tablesorter").tablesorter(); 
		
		} // close init
	} // close namespace
	$.liveace.init();
});
//]]>