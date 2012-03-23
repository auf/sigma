(function ($) {

    var date_re = /(\d{1,2})\/(\d{1,2})\/(\d{4})/

    function parse_date(date_str) {
        var match = date_str.match(date_re);
        if (match) {
            return new Date(match[3], match[2] - 1, match[1]);
        }
        else {
            return null;
        }
    }

    function update_periodes_mobilite() {
        var rows = $('.form-row.date_debut_origine,.form-row.date_debut_accueil');
        rows.each(function () {
            var calculs = $(this).find('.calculs');
            if (calculs.length == 0) {
                calculs = $('<p class="calculs"></p>').appendTo(this);
            }
            var date_debut = parse_date(
                $(this).find('input[name*=date_debut]').val()
            );
            var date_fin = parse_date(
                $(this).find('input[name*=date_fin]').val()
            );
            if (date_debut && date_fin) {
                var nb_mois = date_fin.getMonth() - date_debut.getMonth() +
                    12 * (date_fin.getYear() - date_debut.getYear());
                var nb_jours = Math.round(
                    (date_fin.getTime() - date_debut.getTime()) /
                    (24 * 3600 * 1000)
                );
                calculs.text(nb_jours + ' jours, ' + nb_mois + ' mois.');
            }
            else {
                calculs.text('');
            }
        });
    }

    $(document).ready(function () {
        update_periodes_mobilite();
        $('input[name^=mobilite-0-date]').blur(update_periodes_mobilite);
    });

})(django.jQuery)
