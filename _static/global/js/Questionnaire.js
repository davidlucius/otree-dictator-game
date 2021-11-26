$(document).ready(function() {
    $("div#vaccination-reasons input[type='checkbox']").on("change", function() {
        let num_checked = $("div#vaccination-reasons input:checked").length;
        $("div#vaccination-reasons input[type='checkbox']").each(function() {
            if(num_checked >= 2) {
                if(!$(this).prop("checked")) {
                    $(this).prop("disabled", true);
                }
            } else {
                $(this).prop("disabled", false);
            }
        });
    });
});