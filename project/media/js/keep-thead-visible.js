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

    $(document).ready(function() {
        $(window).scroll(keep_thead_visible);
    });
})(jQuery);
    
