$(document).ready(function() {
    $("div#verlauf input[type='checkbox']").on("change", function() {
        let num_checked = $("div#verlauf input:checked").length;
        $("div#verlauf input[type='checkbox']").each(function() {
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

