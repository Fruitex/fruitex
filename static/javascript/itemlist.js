$(document).ready(function () {
  $(".item-container").hover(function() {
    $(this).children(".btn-add-container").slideDown('fast');
  }, function () {
    $(this).children(".btn-add-container").slideUp('fast');
  });
});