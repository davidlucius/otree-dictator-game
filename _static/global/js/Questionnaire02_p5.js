$(document).ready(function() {
    $("div#warumImpf input[type='checkbox']").on("change", function() {
        let num_checked = $("div#warumImpf input:checked").length;
        $("div#warumImpf input[type='checkbox']").each(function() {
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

