/*!
 * 
 * eConvenor JavaScript collection
 * 
 */


/* Get CSRF token
-------------------------------------------------- */

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

var csrftoken = getCookie('csrftoken');


/* Enable jQuery UI functions
-------------------------------------------------- */

$(function enableJQueryUIFeatures() {
  $('.datepicker').datepicker({ dateFormat: 'yy-mm-dd' });
  $( '.sortable' ).sortable({
    axis: 'y',
    containment: 'parent',
    tolerance: 'pointer',
  });
  $( '.spinner' ).spinner();
});


/* Enable Bootstrap functions
-------------------------------------------------- */
$(function enableBootstrapFeatures() {
  $('.tltip').tooltip({
    placement: 'bottom',
    delay: { show: 500, hide: 100 }
  });
});


/* Enable automatic vertical scrolling to a target
-------------------------------------------------- */

$("html").on("click", "ul li a", function(event){ 
  var $anchor = $(this);
  $("html").stop().animate({
    scrollTop: $($anchor.attr('href')).offset().top-80
  }, 1000);
  event.preventDefault();
});


/* Ajax button handling
-------------------------------------------------- */

$(document).on("click", ".jsbutton", function(){ 
  var button_id = $(this).attr('id');
  var button_data = 'ajax_button=' + button_id;
  saveForm(button_data);
});


/* Update page using AJAX
-------------------------------------------------- */

function updatePage( resp ) {
  $("#ajax-sidebar").html( resp['ajax_sidebar'] );
  $("#ajax-main").html( resp['ajax_main'] );
  $('.tltip').tooltip({
    placement: 'bottom',
    delay: { show: 500, hide: 100 }
  });
  $('.datepicker').datepicker({ dateFormat: 'yy-mm-dd' });
  $( '.sortable' ).sortable({
    axis: 'y',
    containment: 'parent',
    tolerance: 'pointer',
  });
  $( '.spinner' ).spinner();
};

function printError( req, status, err ) {
  console.log( 'There was an AJAX error: ', status, err );
};

function saveForm( button_data ) {
  $('form.savebyjs').each(function() {
    $.ajax({
      data: button_data + '\&' + jQuery(this).serialize(),
      type: "POST",
      dataType: "json",
      success: updatePage,
      error: printError,
      complete: function() {
      },
    });
  });
};


/* Update sidebar labels in real time
-------------------------------------------------- */

$(document).on("keyup change", ".item-heading", function(){ 
  var changed_text = $(this).val();
  var item = $(this).attr('name');
  var item_no = item.split('-', 1);
  var target_id = '#sidebar_heading_' + item_no;
  var replacement_text = item_no + '. ' + changed_text
  $(target_id).text(replacement_text);
});


/* Autosave without page refresh
-------------------------------------------------- */

function autoSave( button_data ) {
  $('form.savebyjs').each(function() {
    $.ajax({
      data: button_data + '\&' + jQuery(this).serialize(),
      type: "POST",
      dataType: "json",
      error: printError,
      complete: function() {
      },
    });
  });
};

$(function() {
  var interval = setInterval("autoSave('ajax_button=save_button')",
    10 * 1000);
});


/* Load AJAX page elements on page refresh
-------------------------------------------------- */

$(function loadAJAXonRefresh() {
  console.log('loadAJAXonRefresh called');
  $.ajax({
    data: 'ajax_button=page_refresh\&csrfmiddlewaretoken=' + csrftoken,
    type: "POST",
    dataType: "json",
    success: updatePage,
    error: printError,
    complete: function() {
      console.log('loadAJAXonRefresh complete');
    },
  });
});


/* Move agenda or minutes item
-------------------------------------------------- */

$(document).on( "sortupdate", function( event, ui ) {
  var sidebar_data = $( ".sortable" ).sortable( "serialize",{
    key: "sidebar"
  });
  sidebar_data = sidebar_data.replace(/&s/g, 's');  
  sidebar_data = sidebar_data.replace(/sidebar=/g, ',');
  sidebar_data = sidebar_data.slice(1);
  var sidebar_string = 'ajax_button=move_item\&new_sidebar_order=' +
    sidebar_data;
  saveForm(sidebar_string);
});
