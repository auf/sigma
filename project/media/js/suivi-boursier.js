(function($) {

    function keep_thead_visible() {
        var windowTop = $(window).scrollTop();
        $('table:not(#keep-thead-visible) thead').each(function() {
            var $table = $(this).closest('table');
            var tableTop = $table.offset().top;
            var tableBottom = tableTop + $table.height();
            if (tableTop < windowTop && tableBottom > windowTop) {
                var $clone = $('#keep-thead-visible');
                if ($clone.length == 0) {
                    $clone = $table.clone()
                        .attr('id', 'keep-thead-visible')
                        .css({
                            position: 'fixed', 'pointer-events': 'none', top: 0,
                            visibility: 'hidden', 'width': $table.width()
                        });
                    $clone.find('thead').css({visibility: 'visible'});
                    $table.after($clone);
                }
            }
            else {
                $('#keep-thead-visible').remove();
            }
        });
    }

    function setup_tbody_toggle() {
        $('table.cachedetails tbody').each(function() {
            var $header = $(this).children('tr').first().children('th').first();
            if ($header.length > 0) {
                var $collapse_link = $('<a href="#"></a>');
                $header.append('(').append($collapse_link).append(')');
                $collapse_link.click(collapse_link_clicked);
                $collapse_link.each(collapse_link_clicked);
            }
        });
    }

    function collapse_link_clicked() {
        var $rows = $(this).closest('tbody').find('tr:not(:first-child)');
        if ($rows.is(':visible')) {
            $rows.hide();
            $(this).text('Détails');
        }
        else {
            $rows.show();
            $(this).text('Cacher les détails');
        }
        $('#keep-thead-visible').remove();
        keep_thead_visible();
        return false;
    }



    $(document).ready(function() {
        $(window).scroll(keep_thead_visible);
        setup_tbody_toggle();
    });

})(jQuery);
    
