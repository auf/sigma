(function($) {
    $(document).ready(function() {
        $('select#id_bareme').change(function() {
            var bareme = $(this).val();
            $('.field-montant_mensuel_origine_sud').hide();
            $('.field-montant_mensuel_accueil_sud').hide();
            $('.field-montant_perdiem_sud').hide();
            $('.field-montant_allocation_unique').hide();
            if (bareme == 'mensuel') {
                $('.field-montant_mensuel_origine_sud').show();
                $('.field-montant_mensuel_accueil_sud').show();
            }
            else if (bareme == 'perdiem') {
                $('.field-montant_perdiem_sud').show();
            }
            else if (bareme == 'allocation') {
                $('.field-montant_allocation_unique').show();
            }
        }).change();
    });
})(django.jQuery)
