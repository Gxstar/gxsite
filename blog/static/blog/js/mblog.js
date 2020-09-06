$(function(){
    $(".bar").click(function() {
        $(".sidebar").animate({left:'0px'},"fast",function(){
            $("#mask").css("visibility","visible");
        });
    });
    $("*:not(.sidebar):not(.bar)").click(function() {
        $(".sidebar").css({left:'-250px'});
        $("#mask").css("visibility","hidden");
    });
});