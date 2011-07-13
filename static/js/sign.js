$(function () {
  $("form#sign_form").submit(function() {
    var nonce = $("form#sign_form #nonce").val();
    var result = document.location.href + "?nonce=" + nonce + "&signature=" +
                 hex_hmac_sha1($("#secret_token").html(), nonce);
    $("#result_url").val(result);
    return false;
  });
});