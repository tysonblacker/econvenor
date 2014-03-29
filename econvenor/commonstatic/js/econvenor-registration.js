/*!
 * 
 * eConvenor Registration JavaScript
 * 
 */


/* Load first registration page
-------------------------------------------------- */

$.get( '/data/people.html', function( html ){
  $( '#target' ).html( html );
});


/* Ajax button handling
-------------------------------------------------- */

$(document).on("click", ".ajax-button", function(){ 
  var button_id = $(this).attr('id');
  loadPage(button_id);
});


/* Update page using AJAX
-------------------------------------------------- */

function updatePage( resp ) {
  $("#ajax-registration").html( resp['ajax_sidebar'] );
  $("#ajax-main").html( resp['ajax_main'] );
  $('.tltip').tooltip({
    placement: 'bottom',
    delay: { show: 500, hide: 100 }
  });
  $('.datepicker').datepicker({
    dateFormat: 'dd M yy',
    onClose: function() {
      $(this).valid();
    },  
  });
  $( '.sortable' ).sortable({
    axis: 'y',
    containment: 'parent',
    tolerance: 'pointer',
  });
  $( '.spinner' ).spinner({ min: 0, max: 600, });
  $('.timepicker').timepicker({
    timeFormat: 'H:i',
    step: 15,
  });
  $('body').css( 'cursor', 'default' );
};

function printError( req, status, err ) {
  console.log( 'There was an AJAX error: ', status + ' / ', err );
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

$(document).on("keyup change", ".item-title", function(){ 
  
  var changed_text = $(this).val();
  var item = $(this).attr('name');
  var item_no = item.split('-', 1);
  item_no = item_no[0];
  item_no = item_no.substr(1);
  var target1_text = changed_text;
  var target2_text = changed_text.substr(0,35);
  var target1 = '#panel_heading_' + item_no;
  $(target1).text(target1_text);
  var target2 = '#sidebar_heading_' + item_no;
  $(target2).text(target2_text);
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

function saveWithoutRefresh( button_data, next_page ) {
  $('form.savebyjs').each(function() {
    $.ajax({
      data: button_data + '\&' + jQuery(this).serialize(),
      type: "POST",
      dataType: "json",
      success: function() {
        if ( next_page )
          document.location.href = next_page
      },
      error: printError,
      complete: function() {
      },
    });
  });
};


/* Activate autosave
-------------------------------------------------- */

$(function() {
  var interval = setInterval("saveWithoutRefresh('ajax_button=save_agenda')",
    3600 * 1000);
});
