$(document).ready(function() {
    if ($('#filter .datepicker').length > 0) {
        $('#filter #t0').datetimepicker({
            format: 'YYYY-MM-DD',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
        $('#filter #t1').datetimepicker({
            format: 'YYYY-MM-DD',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
    }
    
    if ($('#filter .datetimepicker').length > 0) {
        $('#filter #t0').datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
        $('#filter #t1').datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            allowInputToggle: true,
            showTodayButton: true,
            sideBySide: true,
        });
    }
});