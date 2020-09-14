$(function () {
    jump = function (page) {
        var a={};
        $.ajax({
            type: "GET",
            url: "get_new_comment",
            dataType: "json",
            data: {
                page: page
            },
            async:false,
            success: function (result) {
                console.log(result);
                a=result;
            },
        });
        console.log(a);
    }
})