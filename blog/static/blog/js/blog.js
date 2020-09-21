$(function () {
    replace_com = function (a) {
        // 替换评论列表
        $("div.com").remove();
        a.comments.forEach(element => {
            author = element.fields.author;
            body = element.fields.body;
            var com = $("<div class='com'></div>");
            var eauthor = $("<div class='com-author'></div>").append("<p>" + author + "</p>");
            var ebody = $("<div class='com-body'></div>").append("<p>" + body + "</p>");
            com.append(eauthor);
            com.append(ebody);
            $('#com-header').after(com);
        });
    };
    jump = function (page, element) {
        // page是要跳转的页码，element是要跳转页码的li元素
        // 评论按钮跳转方法
        var a = {};
        $.ajax({
            type: "GET",
            url: "get_new_comment",
            dataType: "json",
            data: {
                page: page
            },
            async: false,
            success: function (result) {
                a = result;
            },
        });
        $("#page-list>li").removeClass("active");
        $(element).addClass("active");
        replace_com(a);
    };
    $("#front").click(function(){
        // 处理前一页按钮
        var loc=parseInt($("#page-list .active").text());
        if (loc<=first) {
            alert('已经是第一页了！');
        } else {
            loc=loc-1;
            jump(loc,$("#pagenum"+loc));
        }
    });
    $("#next").click(function(){
        // 处理后一页按钮
        var loc=parseInt($("#page-list .active").text());
        if (loc==parseInt($("#page-list>li").eq(-2).text())) {
            alert('已经是最后一页了！');
        } else {
            loc=loc+1;
            jump(loc,$("#pagenum"+loc));
        }
    });
    $("#subbtn").click(function(){
        // 点击提交评论
        var result={};
        $.ajax({
            type: "POST",
            url: "new_comment/",
            dataType: "json",
            data: {
                username:$('#id_username').val(),
                email:$('#id_email').val(),
                body:$('#id_body').val(),
                captcha_1: $('#id_captcha_1').val(),
                captcha_0: $('#id_captcha_0').val(),
            },
            async: false,
            success: function (result) {
                a = result;
            },
        });
    });
})