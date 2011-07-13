var moreButton = function(div, name) {
  var more = $("<p><a href='#'>More</a></p>");
  div.append(more);
  more.click(function() {
    var removeLink = $('<a href="#" class="remove">-</a>');
    var toAdd = $('<span/>');
    toAdd.append($('<br/><input type="text" name="' + name + '[]">')).append(removeLink);
    more.before(toAdd);
    return false;
  });
}

$(function() {
  moreButton($("form div#identifiers"), "identifiers");
  moreButton($("form div#circles"), "circles");
  $("a.remove").live("click", function() {
    $(this).parent("span").remove();
    return false;
  });
  
  function toCapText(list) {
    return $.map(list, function(x) { return "<span style='text-transform: capitalize'>" + x +  "</span>"});
  }
  
  $.history.init(function(hash) {
    if (match = hash.match(/^\/circles\/(.*)/)) {
      $.getJSON(hash, function(data) {
        var details = $("#circle_details");
        details.html("<h3>" + $("a[href='#" + hash + "']").html() + "</h3>");
        var list = $("<ul/>");
        details.append(list);
        for (person in data["people"]) {
          person = data["people"][person];
          list.append("<li><a href='/p/" + person.key + "/edit'>" + person.name + "</a> " +
                "(<a href='" + person.identifiers[0] + "'>" + person.identifiers[0] + "</a>) - " +
                toCapText(person.circles).join(", ") + "</li>");
        }
      });
    }
  });
});