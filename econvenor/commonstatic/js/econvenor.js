/*!
 * 
 * eConvenor base JavaScript
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
});


/* Enable Bootstrap functions
-------------------------------------------------- */
$(function enableBootstrapFeatures() {
  $('.tltip').tooltip({
    placement: 'bottom',
    delay: { show: 500, hide: 100 }
  });
});


/* Enable Timepicker
-------------------------------------------------- */
$(function enableTimepicker() {
  $('.timepicker').timepicker({
    'timeFormat': 'g:i a',
    'step': 15,
    'scrollDefaultTime': '9:15 am',
  });
});


/* Enable automatic vertical scrolling to a target
-------------------------------------------------- */

$("html").on("click", ".sidebar-heading", function(event){ 
  var $anchor = $(this);
  $("html").stop().animate({
    scrollTop: $($anchor.attr('href')).offset().top-90
  }, 1000);
  event.preventDefault();
});


/* Enable zooming of images
-------------------------------------------------- */

$(document).on("click", ".zoom-button", function(){ 
  var current_zoom = $('.zoomable').attr('width');
  current_zoom = current_zoom.slice(0, -1);
  current_zoom = parseInt(current_zoom, 10)
  var zoom_direction = $(this).attr('id');
  if (zoom_direction == 'zoom_out') {
    new_zoom = current_zoom - 10;
    } else {
    new_zoom = current_zoom + 10;
    }
  var zoom = new_zoom + '%'
  $('.zoomable').attr('width', zoom);
});


/* Clear distribution list checkboxes when required
-------------------------------------------------- */

$(document).on("click", ".checkbox #all_participants", function(){ 
  var checkbox_status = $(this).prop('checked');
  if (checkbox_status == true) {
    $(".individual-checkbox").prop('checked', false);
  };
});

$(document).on("click", ".individual-checkbox", function(){ 
  var checkbox_status = $(this).prop('checked');
  if (checkbox_status == true) {
    $(".checkbox #all_participants").prop('checked', false);
  };
});


/* Populate deletion confirmation modal
-------------------------------------------------- */

$(document).on("click", ".delete-button", function(event){ 
  event.preventDefault();
  var instruction = $(this).attr('id');
  var description = $(this).attr('name');
  var confirmation_message = '<p>You are about to delete this record:\
    <br/><br/><strong>' + description + '</strong><br/><br/>\
    This action cannot be undone.<br/><br/>Continue?</p>';
  $('.modal-button').attr('value', instruction);
  $(".modal-body").html( confirmation_message );
  $('#delete_modal').modal();
});


/* Enable dynamic sidebar navigation
-------------------------------------------------- */

$(function() {
  $("#leftsidebar").metisMenu();
});

$(function removeActiveItemCarat() {
  $(".active a:nth-child(1) i:nth-child(2)").toggleClass("fa-angle-down fa-angle-up");
});

$(".sidebar-item ").click(function() {
  	var item_clicked_arrow = $(this).children().first().children().next()
  	$("i").filter(".fa-angle-up").not(item_clicked_arrow).toggleClass(
  	  "fa-angle-down fa-angle-up"
  	);
  	item_clicked_arrow.toggleClass("fa-angle-down fa-angle-up");
});


/* Character counter/limiter plugin 
-------------------------------------------------- */

$(function() {

  $.fn.charactercounter = function(){

    var char_counter_div = $("<div class='characterCounterDisplay pull-right'/>");
    this.before(char_counter_div);
    $(".characterCounterDisplay").hide();

    /* This valHook is necessary to get the .val() to correctly count newlines 
       are two characters and not one */
    $.valHooks.textarea = {
      get: function( elem ) {
        return elem.value.replace( /\r?\n/g, "\r\n" );
      }
    };

    this.on("focus keyup", function(){ 
      var char_count = $(this).val().length;
      var maximum_length = $(this).attr('maxlength');
      if (char_count > maximum_length) {
        var trimmed_text = $(this).val().substr(0, maximum_length);
        $(this).val(trimmed_text);
        char_count = maximum_length;
      };
      var warning_length = parseInt(maximum_length * 0.18) * 5
      var chars_remaining = maximum_length - char_count;
      if (char_count == 0) {
        var message = "<p>" + chars_remaining + ' characters maximum</p>'
      } else {
        var message = "<p>" + chars_remaining + ' characters remaining</p>'
      };
      $(".characterCounterDisplay").html( message );
      if ((char_count >= warning_length) || (char_count === 0)) {
        ($(this)).prev().addClass("red");
      } else {
        ($(this)).prev().removeClass("red");  
      };
      $($(this)).prev().show();
    });

    this.on("blur", function(){ 
      $(".characterCounterDisplay").hide();
    });

  };
});

/* Enable character counter/limiter
-------------------------------------------------- */

$(function() {
  $('.charactercounter').charactercounter();
});


/* Location field formatter 
-------------------------------------------------- */

$(function() {

  $.fn.locationformatter = function(){

    String.prototype.insert = function (index, string) {
      return this.substring(0, index) + string + this.substring(index, this.length);
    };

    var countNewLines = function ( elem ) {
      var newlines = elem.val().match(/\r\n/g);
      if (newlines) {
        var no_of_newlines = newlines.length;
      } else {
        var no_of_newlines = 0;
      };
      return no_of_newlines;
    }
    
    this.on("focus keyup", function(){ 
      var maximum_line_length = 30;
      var maximum_new_lines = 1;
      /* Calculate length of first line */
      var first_line = $(this).val().split(/\r\n/).slice(0,1)[0];
      if (first_line) {
        var first_line_count = first_line.length;
      } else {
        var first_line_count = 0;
      };
      /* Cap the number of characters in the first line at 30 */
      if (first_line_count >= maximum_line_length) {
        var new_string = $(this).val().insert((maximum_line_length-1), "\r\n");
        $(this).val(new_string);
      };
      /* Forbid more than one newline character */
      newline_count = countNewLines($(this));
      if (newline_count > 1) {
        var strings = $(this).val().split(/\r\n/);
        strings.splice(1, 0, "\r\n");
        var new_string = strings.join("");
        $(this).val(new_string);
        newline_count = countNewLines($(this));
      };
      /* Calculate length of second line*/
      if (newline_count > 0) {
        var second_line = $(this).val().split(/\r\n/).slice(1,2)[0];
        var second_line_count = second_line.length;
      };
      /* Trim the number of characters in the second line at 30 if necessary*/
      if ((newline_count > 0) && (second_line_count >= maximum_line_length)) {
        var first_line = $(this).val().split(/\r\n/).slice(0,1)[0];
        var second_line = second_line.slice(0,maximum_line_length);
        var new_string = first_line + second_line;
        $(this).val(new_string);
      };
      /* Populate and show the character counter message */
      var first_line = $(this).val().split(/\r\n/).slice(0,1)[0];
      var second_line = $(this).val().split(/\r\n/).slice(1,2)[0];
      if (first_line) {
        var line1_chars_left = maximum_line_length - first_line.length;
      } else {
        var line1_chars_left = maximum_line_length;
      };
      if (second_line) {
        var line2_chars_left = maximum_line_length - second_line.length;
      } else {
        var line2_chars_left = maximum_line_length;
      };
      var message = "<p>Line 1: " + line1_chars_left + ' chars left / Line 2: ' + line2_chars_left + ' chars left</p>'
      $(".characterCounterDisplay").html( message );
    });

  };
});


/* Enable location field formatter
-------------------------------------------------- */

$(function() {
  $('.locationformatter').locationformatter();
});


/* Remover of double newlines 
-------------------------------------------------- */

$(function() {

  $.fn.newlinecontrol = function(){

    this.on("focus keyup", function(){
      var raw_text = $(this).val();
      var doublenewline = $(this).val().match(/\r\n\r\n/g);
      if (doublenewline) {
        var clean_text = raw_text.replace( /\r\n\r\n/, "\r\n" );
        var message = "<p>Space between paragraphs added automatically</p>";
        $(".characterCounterDisplay").html( message );
        $(".characterCounterDisplay").addClass("red");
        $(this).val(clean_text);
      };
    });

  };
});


/* Enable remover of double newlines 
-------------------------------------------------- */

$(function() {
  $('.charactercounter').newlinecontrol();
});


/* Manage tip box in sidebar
-------------------------------------------------- */

function renderTip(tip_number) {
  var tip_area = $("#tip_area").html();
  var tip_id = "#tip_body_" + tip_number;
  var tip_body = $(tip_id).html();
  var tip_heading = tip_area + ': Tip #' + tip_number;
  $("#tip_heading").html(tip_heading);
  $("#tip_body").html(tip_body);
};

function showNextTip() {
  var tip_heading = $("#tip_heading").html();
  if (tip_heading) {
    if ( tip_heading.length ) {
      var current_tip_number = parseInt(tip_heading.split("#")[1]);
      var next_tip_number = current_tip_number + 1;
      var next_tip_id = "#tip_body_" + next_tip_number;
      var next_tip_body = $(next_tip_id).html();
      if ( !next_tip_body ) {
        next_tip_number = 1;
      };
    } else {
      var next_tip_number = 1;
    };
  } else {
    var next_tip_number = 1;
  };
  renderTip(next_tip_number);
};

function showPreviousTip() {
  var tip_heading = $("#tip_heading").html();
  var current_tip_number = parseInt(tip_heading.split("#")[1]);
  var previous_tip_number = current_tip_number - 1;
  if ( previous_tip_number < 1 ) {
    var previous_tip_number = 1;
  };
  renderTip(previous_tip_number);
};

function setTipInterval() {
  tip_interval = setInterval("showNextTip()", 15 * 1000);
};

$("#next_tip").click(function jumpToNextTip() {
    clearInterval(tip_interval);
    showNextTip();
    setTipInterval();
});

$("#previous_tip").click(function jumpToPreviousTip() {
    clearInterval(tip_interval);
    showPreviousTip();
    setTipInterval();
});

$(function initialiseTipBox() {
  showNextTip();
  setTipInterval();
});


/* Force email addresses to lower case
-------------------------------------------------- */

$('.email').on("keyup", function(){
  $(this).val($(this).val().toLowerCase());
});
