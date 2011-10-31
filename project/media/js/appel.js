(function($) {
    $(document).ready(function() {
        $('select#id_bareme').change(function() {
            var bareme = $(this).val();
            $('.form-row.montant_mensuel_origine_sud').hide();
            $('.form-row.montant_mensuel_accueil_sud').hide();
            $('.form-row.montant_perdiem_sud').hide();
            $('.form-row.montant_allocation_unique').hide();
            if (bareme == 'mensuel') {
                $('.form-row.montant_mensuel_origine_sud').show();
                $('.form-row.montant_mensuel_accueil_sud').show();
            }
            else if (bareme == 'perdiem') {
                $('.form-row.montant_perdiem_sud').show();
            }
            else if (bareme == 'allocation') {
                $('.form-row.montant_allocation_unique').show();
            }
        }).change();
    });
})(django.jQuery)
