$(document).ready(function(){
$('.table').paging({limit:7});
NProgress.start();
NProgress.done();
$(".datetimeinput").datepicker({changeYear: true,changeMonth: true, dateFormat: 'yy-mm-dd'});


});