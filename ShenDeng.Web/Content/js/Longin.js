function login(){
    var username = document.getElementByName("UserName").value;
    var password = document.getElementByName("PassWord").value;
    if(username==""){
        $.jGrowl("用户名不能为空！", { header: '提醒' });
    }else if(password==""){
        $.jGrowl("密码不能为空！", { header: '提醒' });
    } else {
        //location.href = '/Login/LogOff'; 
        //AjaxFunc();
    }
}
function AjaxFunc()
{
    var username = document.getElementById("ID").value;
    var password = document.getElementById("PASSWORD").value;
    $.ajax({
        type: 'post',
        url: "Account/Login",
        dataType: "json",
        data: {"username": username,"password": password},
        success: function (data) {
            
        },
        error: function (xhr, type) {
            console.log(xhr);
        }
    });
}