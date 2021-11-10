$(document).ready(function() {
    $("input#id_taler").on("input", function() {
        let points_for_partner = js_vars.endowment_in_points - parseInt($(this).val());
        $("#points-for-partner").text(
            0 <= points_for_partner && points_for_partner <= js_vars.endowment_in_points ? points_for_partner : "___"
        );
    });
});