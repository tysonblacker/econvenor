/*!
 * 
 * eConvenor JavaScript collection
 * 
 */


/* Resolve button conflict issue
-------------------------------------------------- */

var bootstrapButton = $.fn.button.noConflict()
  $.fn.bootstrapBtn = bootstrapButton 


/* Enable DatePicker
-------------------------------------------------- */

$(function() {
  $('.datepicker').datepicker({ dateFormat: "yy-mm-dd" });
});


/* Automatic vertical scrolling
-------------------------------------------------- */

$(function() {
  $('ul li a').bind('click',function(event){
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: $($anchor.attr('href')).offset().top-80
    }, 1000);
    event.preventDefault();
  });
});


/* Save a form
-------------------------------------------------- */

function saveform() {
  $('form.autosave').each(function() {
    $.ajax({
      data: 'save_items_button=save_items\&'+jQuery(this).serialize(),
      type: "POST",
      success: function(data){
        if(data && data == 'success') {alert('Success');}else{alert('Autosave may have failed');}
      }
    });
  });
}


/* Run scripts periodically
-------------------------------------------------- */

setInterval(saveform, 600 * 1000);

