/*!
 * 
 * eConvenor JavaScript collection
 * 
 */


/* Resolve button conflict issue
-------------------------------------------------- */

$(function() {
  $.widget.bridge('uibutton', $.ui.button);
});


/* Get CSRF token
-------------------------------------------------- */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


/* Enable DatePicker
-------------------------------------------------- */

$(function() {
  $('.datepicker').datepicker({ dateFormat: "yy-mm-dd" });
});


/* Enable tooltips
-------------------------------------------------- */
$(function() {
  $('.tltip').tooltip({placement: 'bottom', delay: { show: 500, hide: 100 }});
});


/* Automatic vertical scrolling
-------------------------------------------------- */

$("html").on("click", "ul li a", function(event){ 
  var $anchor = $(this);
  $("html").stop().animate({
    scrollTop: $($anchor.attr('href')).offset().top-80
  }, 1000);
  event.preventDefault();
});


/* Save a form
-------------------------------------------------- */

function updatePage( resp ) {
  $("#ajax-sidebar").html( resp['ajax_sidebar'] );
  $("#ajax-items").html( resp['ajax_items'] );
  $('.tltip').tooltip({placement: 'bottom', delay: { show: 500, hide: 100 }});
  $( ".spinner" ).spinner();
  $( ".sortable" ).sortable({ axis: "y", containment: "parent", tolerance: "pointer", });
  
};

function printError( req, status, err ) {
  console.log( 'Save error: ', status, err );
};

function saveform( button_data ) {
  $('form.savebyjs').each(function() {
    $.ajax({
      data: button_data + '\&' + jQuery(this).serialize(),
      type: "POST",
      dataType: "json",
      success: updatePage,
      error: printError,
      complete: function() {
        console.log('saveform complete');
      },
    });
  });
};


/* Agenda button handling
-------------------------------------------------- */

$(document).on("click", ".jsbutton", function(){ 
    console.log( 'button press registered!' );
    var button_id = $(this).attr('id');
     console.log( 'button id: ' + button_id );
    var button_data = 'ajax_button=' + button_id;
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


/* Autosave
-------------------------------------------------- */

function autosave( button_data ) {
  $('form.savebyjs').each(function() {
    $.ajax({
      data: button_data + '\&' + jQuery(this).serialize(),
      type: "POST",
      dataType: "json",
      success: {},
      error: printError,
      complete: function() {
        console.log('autosave complete');
      },
    });
  });
};


$(function() {
  var interval = setInterval("autosave('ajax_button=save_button')",
    3600 * 1000);
  console.log('Autosave has been initialised');
});


/* Load AJAX page elements on page refresh
-------------------------------------------------- */

$(function() {
  $.ajax({
    data: 'ajax_button=page_refresh\&csrfmiddlewaretoken=' + csrftoken,
    type: "POST",
    dataType: "json",
    success: updatePage,
    error: printError,
    complete: function() {
      console.log('initial data complete');
    },
  });
});


/* Enable spinners and sortable lists
-------------------------------------------------- */

$(function() {
  $( ".spinner" ).spinner();
  $( ".sortable" ).sortable({ axis: "y", containment: "parent", tolerance: "pointer", });
});


/* Move agenda or minutes item
-------------------------------------------------- */

$(document).on( "sortupdate", function( event, ui ) {
  var sidebar_data = $( ".sortable" ).sortable( "serialize", { key: "sidebar" } );
  sidebar_data = sidebar_data.replace(/&s/g, 's');  
  sidebar_data = sidebar_data.replace(/sidebar=/g, ',');
  sidebar_data = sidebar_data.slice(1);
  var sidebar_string = 'ajax_button=move_item\&new_sidebar_order=' + sidebar_data;
  console.log(sidebar_string);
  saveform(sidebar_string);
});



