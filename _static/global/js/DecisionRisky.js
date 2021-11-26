$(document).ready(function() {
    $("select#id_appointment").on("change", function() {
        let selected_option = $(this).val() ? parseInt($(this).val()) : null;
        $("span#additional-amount").text(
            selected_option ? js_vars.options[selected_option].amount : "___");
        $("span#total-amount").text(
            selected_option ? js_vars.options[selected_option].amount + js_vars.endowment_in_points : "___");
        if(js_vars.round_number == 2) {
            $("span#failure-amount").text(
                selected_option ? js_vars.failure_payoff : "___");
        }
        $("span#probability").text(
            selected_option ? js_vars.options[selected_option].probability : "___");
    });
});