$(function () {
    replace_com = function (a) {
        // 替换评论列表
        $("div.com").remove();
        $("li.pageicon").remove();
        a.comments.reverse().forEach(element => {
            author = element.fields.author;
            time = element.fields.createTime;
            body = element.fields.body;
            var com = $("<div class='com'></div>");
            var eauthor = $("<div class='com-author'></div>").append("<p>昵称：" + author + "</p><p>评论于" + time + "</p>");
            var ebody = $("<div class='com-body'></div>").append("<p>" + body + "</p>");
            com.append(eauthor);
            com.append(ebody);
            $('#com-header').after(com);
        });
        a.page_list.forEach(element => {
            var icon=$(`<li id=pagenum${element} onclick='jump(${element},this)' class='pageicon'>${element}</li>`);
            $("#next").before(icon);
        })
    };
    jump = function (page, element) {
        // page是要跳转的页码，element是要跳转页码的li元素
        // 评论按钮跳转方法
        var a = {};
        var mark=$(element).attr('id');
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
        replace_com(a);
        $("#"+mark).addClass("active");
    };
    $("#front").click(function () {
        // 处理前一页按钮
        var loc = parseInt($("#page-list .active").text());
        if (loc <= first) {
            alert('已经是第一页了！');
        } else {
            loc = loc - 1;
            jump(loc, $("#pagenum" + loc));
        }
    });
    $("#next").click(function () {
        // 处理后一页按钮
        var loc = parseInt($("#page-list .active").text());
        if (loc == parseInt($("#page-list>li").eq(-2).text())) {
            alert('已经是最后一页了！');
        } else {
            loc = loc + 1;
            jump(loc, $("#pagenum" + loc));
        }
    });
    $("#subbtn").click(function () {
        // 点击提交评论
        var a = {};
        $.ajax({
            type: "POST",
            url: "new_comment/",
            dataType: "json",
            data: {
                username: $('#id_username').val(),
                email: $('#id_email').val(),
                body: $('#id_body').val(),
                captcha_1: $('#id_captcha_1').val(),
                captcha_0: $('#id_captcha_0').val(),
            },
            async: false,
            success: function (result) {
                a = result;
            },
        });
        if (a.status == 1) {
            alert('评论添加成功！');
            jump(1, $('#page-list>li:eq(1)'));
            $(".content_in").val("");
        } else {
            alert('验证码错误！请点击图片刷新');
        }
    });
})