$(function() {

	var outfits = $(".outfit");
	var btn = $("input[type='button']");
	console.log(btn);
	outfits.not(':first').hide();
	
	btn.on("click", function() {

		outfits.stop(true, true);
		outfits.filter(":visible").fadeOut(500, function() {
			console.log($(this));
			next = $(this).next(".outfit");
			if(next.length > 0) {
				next.fadeIn(500);
			} else {
				outfits.first().fadeIn(500);
			}
		});
	});
});