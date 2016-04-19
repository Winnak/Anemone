$(document).ready(function() {
    jQuery.timeago.settings.allowPast = true;
    jQuery.timeago.settings.allowFuture = true;
  $("time.timeago").timeago();
});
