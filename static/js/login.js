/**
 * Created by xuJL on 2017/7/28.
 */

$(document).ready(function () {
    $("#id_username").focus();
});

// 点击一次,更改图片内容,
function ChangeCode(ths) {
    ths.src = ths.src + '?';
}

function ClearFocus(tagId) {
    var item = $('#'+tagId);
    item.val("");
    item.focus();
}

$(function () {
    $("#id_check_code").blur(function () {
        $("#error_code").empty();
    });
    $("#id_password").blur(function () {
        $("#error_pass").empty();
    });

    $('#id_form').submit(function(){
    var name = $("#id_username").val();                 //获得form中用户输入的name 注意这里的id_name 与你html中的id一致
    var password = $("#id_password").val();    //同上
    var code = $("#id_check_code").val();
    console.log(name,password,code);

    $.ajax({
        type:"POST",
        data: {username:name, password:password, checkcode:code},
        url: ".", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
        cache: false,
        dataType: "html",
        async:true,

        success: function(msg){
            var scheme = window.location.protocol;
            var host = window.location.host;
            if(msg ==="admin"){
                window.location.href= scheme+"//"+host+"/admin/";
            }else {
                window.location.href= scheme+"//"+host+"/accounts/"
            }
        },

        error: function(msg){
            state = msg.responseText.trim();
            var password = $('#id_password');
            var code = $('#id_check_code');
            $(".logimg").click();
            if(state ==="password"){
                $("span[id='error_pass']").text("用户名或密码错误");
                password.val("");
                code.val("");
                password.focus();
            }else{
                if(state ==="checkcode-expired"){
                    $("span[id='error_code']").text("验证码失效");

                }else {
                    $("span[id='error_code']").text("验证码错误");
                }
                code.val("");
                code.focus();

            }
        }
    });
    return false;
});
});





