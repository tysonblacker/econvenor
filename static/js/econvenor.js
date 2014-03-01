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

$(document).on("click", "ul li a", function(event){ 
  var $anchor = $(this);
  $("html").stop().animate({
    scrollTop: $($anchor.attr('href')).offset().top-80
  }, 1000);
  event.preventDefault();
});


/* Save a form
-------------------------------------------------- */

function updatePage( resp ) {
  $("#ajax").html( resp );
};

function printError( req, status, err ) {
  console.log( 'Something went wrong: ', status, err );
};

function saveform( button_data ) {
  $('form.savebyjs').each(function() {
    $.ajax({
      data: button_data + '\&' + jQuery(this).serialize(),
      type: "POST",
      dataType: "html",
      success: updatePage,
      error: printError
    });
  });
};


/* Agenda button handling
-------------------------------------------------- */

$(document).on("click", ".jsbutton", function(){ 
    console.log( 'button press registered!' );
    var button_id = $(this).attr('id');
     console.log( 'button id: ' + button_id );
    var button_data = 'agenda_button=' + button_id;
    saveform(button_data);
});


/* Update sidebar labels
-------------------------------------------------- */

$(document).on("keyup change", ".item-heading", function(){ 
  var changed_text = $(this).val();
  var item = $(this).attr('name');
  var item_no = item.split('-', 1);
  var target_id = '#sidebar_heading_' + item_no;
  var replacement_text = item_no + '. ' + changed_text
  $(target_id).text(replacement_text);
});


/* Run scripts periodically
-------------------------------------------------- */

setInterval(function () {
                saveform('agenda_button=save_button');
            }, 120 * 1000);
