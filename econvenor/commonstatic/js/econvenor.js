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

$("html").on("click", ".sidebar-heading", function(event){ 
  var $anchor = $(this);
  $("html").stop().animate({
    scrollTop: $($anchor.attr('href')).offset().top-80
  }, 1000);
  event.preventDefault();
});
