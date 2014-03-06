/*!
 * 
 * eConvenor AJAX JavaScript
 * 
 */


/* Load AJAX page elements on page refresh
-------------------------------------------------- */

$(function loadAJAXonRefresh() {
  $.ajax({
    data: 'ajax_button=page_refresh\&csrfmiddlewaretoken=' + csrftoken,
    type: "POST",
    dataType: "json",
    success: updatePage,
    error: printError,
    complete: function() {
    },
  });
});


/* Ajax button handling
-------------------------------------------------- */

$(document).on("click", ".ajax-button", function(){ 
  $('body').css( 'cursor', 'wait' );
  var button_id = $(this).attr('id');
  var button_data = 'ajax_button=' + button_id;
  saveForm(button_data);
});

$(document).on("click", ".navigate-button", function(){ 
  saveWithoutRefresh('ajax_button=save_button');
  var new_page = $(this).attr('goto');
  document.location.href = new_page;
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
  $( '.spinner' ).spinner({ min: 0, max: 600, });
  $('body').css( 'cursor', 'default' );
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


/* Move agenda or minutes item
-------------------------------------------------- */

$(document).on( "sortupdate", function( event, ui ) {
  $('body').css( 'cursor', 'wait' );
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


/* Save without page refresh
-------------------------------------------------- */

function saveWithoutRefresh( button_data ) {
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


/* Activate autosave
-------------------------------------------------- */

$(function() {
  var interval = setInterval("saveWithoutRefresh('ajax_button=save_button')",
    30 * 1000);
});
