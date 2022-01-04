$(document).ready(function() {
    $("div#gegenImpfung input[type='checkbox']").on("change", function() {
        let num_checked = $("div#gegenImpfung input:checked").length;
        $("div#gegenImpfung input[type='checkbox']").each(function() {
            if(num_checked >= 4) {
                if(!$(this).prop("checked")) {
                    $(this).prop("disabled", true);
                }
            } else {
                $(this).prop("disabled", false);
            }
        });
    });
});

