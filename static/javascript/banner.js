var SearchBox = function() {
  var submitQuery = function() {
    var query = '';
    if ($(".cate_tag").length) {
      query = 'cate:\'' + $(".cate_tag").text() + '\'';
    }
    query += ' store:' + GetSelectedStore() + ' ';
    query += $('#search-input')[0].value;
    window.location = '/home/?query=' + encodeURIComponent(query);
  };

  var createCateTag = function(value) {
    var closeBtn = $("<img>").attr("src", "{% static "imgs/btn_cross.png" %}");
    closeBtn.click(function () {
      $(this).parent().remove();
      submitQuery();
    });
    return $("<span>").text(value).addClass("cate-tag").append(closeBtn);
  };

  var initSearchBox = function() {
    $('#search-btn').click(function() {
      submitQuery();
    });
    $("#search-input-wrapper").remove(".cate_tag");
    var query = getURLParameter('query');
    if (query) {
      var parsedQuery = ParseQuery(query);
      if (parsedQuery.cate && parsedQuery.cate.length) {
        // FIXME: Add support for multiple cates
        var tag = createCateTag(parsedQuery.cate[0]);
        $("#search-input-wrapper").prepend(tag);
        setTimeout(function(){
          // Avoid racing between js and browser rendering
          $("#search-input").css("width", 460 - tag.width() + 'px');
        },0);
      }
      if (parsedQuery.store &&
          parsedQuery.store.length &&
          parsedQuery.store[0]) {
        $('.store-name').text(GetSelectedStoreDisplay());
        $('.store-tag').css('display', 'inline-block');
      }

      if (parsedQuery.keyword) {
        $("#search-input").val(parsedQuery.keyword);
      }
    }
    $("#search-input").keyup(function (evt) {
      if (evt.which == 13) {
        submitQuery();
      }
    })
    $('.center-container').fadeIn();
  };

  return {
    init: initSearchBox
  };
}();
