document.addEventListener('DOMContentLoaded', function () {
  particleground(document.getElementById('particles'), {
    dotColor: '#5cbdaa',
    lineColor: '#5cbdaa'
  });
  var intro = document.getElementById('intro');
  intro.style.marginTop = - intro.offsetHeight / 2 + 'px';
}, false);

function regist_move(){
        $('#username').fadeIn();
        $('#level').fadeIn();
        $('#login-submit').hide();
        $('#login-submit-move').show();
        $('#password_check').show();
        $('#password_check').css('margin-top','5px');
        $('#password_notice').show();
        $('#password').css('margin-bottom','0px');
        $('#regist-submit').show();
        $('#regist-submit-move').hide();
        $('#email').val('');
        $('#password').val('');
        $('#username').val('');
        $('#mode').text('regist');
}

function login_move(){
        $('#username').fadeOut();
        $('#level').fadeOut();
        $('#rollback-submit').hide();
        $('#regist-submit').hide();
        $('#regist-submit-move').show();
        $('#login-submit-move').hide();
        $('#login-submit').show();
        $('#password_notice').hide();
        $('#password_check').hide();
        $('#password').css('margin-bottom','10px');
        $('#email').val('');
        $('#password').val('');
        $('#password_check').val('');
        $('#username').val('');
        $('#level').val('none');
        $('#mode').text('login');
}

function login(){
    var email = $('#email').val();
    var password = $('#password').val();
    var mode = $('#mode').text();
    var csrf = $('#csrf').text();

    var lock = 0;

    if (email.length == 0){
        swal("알림", "이메일을 입력해주세요", "info");
        lock = 1;
    }
    else if (password.length == 0){
        swal("알림", "비밀번호를 입력해주세요", "info");
        lock = 1;
    }

    console.log("email ----> " + email);
    console.log("password ----> " + password);
    console.log("mode ----> " + mode);
    console.log("csrf ----> " + csrf);
    console.log("lock ----> " + lock);

    if(lock == 0){
    $.post( "/login", {
       email: email,
       password: password,
       mode: mode,
       csrfmiddlewaretoken: csrf,
     })
      .done(function( data ) {
          if(data.return == '0'){
              window.location.href = "/main/1";
          }
          else if(data.return == '999'){
              window.location.href = "/admin";
          }
          else if(data.return == '1'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '2'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '3'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '5'){
              swal("알림", "아이디나 패스워드가 일치하지 않습니다.", "info");
          }
      });
    }
}

function regist(){
    var email = $('#email').val();
    var password = $('#password').val();
    var password_check = $('#password_check').val();
    var username = $('#username').val();
    var level = $('#level').val();
    var mode = $('#mode').text();
    var csrf = $('#csrf').text();

    var lock = 0;

    console.log(email.length);

    if (email.length == 0){
        swal("알림", "이메일을 입력해주세요", "info");
        lock = 1;
    }
    else if (email.indexOf("@") == -1){
        swal("알림", "올바른 이메일을 입력해주세요", "info");
        lock = 1;
    }
    else if (password.length == 0){
        swal("알림", "비밀번호를 입력해주세요", "info");
        lock = 1;
    }
    else if (username.length == 0){
        swal("알림", "사용자 이름을 입력해주세요", "info");
        lock = 1;
    }
    else if (level == 'none'){
        swal("알림", "일본어 수준을 선택해주세요", "info");
        lock = 1;
    }

    console.log("email ----> " + email);
    console.log("password ----> " + password);
    console.log("password_check ----> " + password_check);
    console.log("username ----> " + username);
    console.log("level ----> " + level);
    console.log("mode ----> " + mode);
    console.log("csrf ----> " + csrf);

    if(lock == 0){
    $.post( "/regist", {
       email: email,
       password: password,
       password_check: password_check,
       username: username,
       level: level,
       mode: mode,
       csrfmiddlewaretoken: csrf,
     })
      .done(function( data ) {
          if(data.return == '0'){
              swal("알림", "회원가입 되신걸 축하드립니다", "success");
              login_move();
          }
          else if(data.return == '1'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '2'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '3'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '4'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '5'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '6'){
              swal("경고", "불법적인 접근입니다. 패킷을 수정하지 마세요", "error");
          }
          else if(data.return == '50'){
              swal("알림", "확인된 패스워드가 다릅니다.\n 패스워드를 일치하게 입력해주세요", "info");
          }
          else if(data.return == '99'){
              swal("알림", "중복된 이메일입니다. 다른 이메일로 가입해주세요", "info");
          }
      });
    }
}

$(document).ready(function(){

    $("input[name=email]").keydown(function (key) {
        if(key.keyCode == 13){
            login();
        }
    });

    $("input[name=password]").keydown(function (key) {
        if(key.keyCode == 13){
            login();
        }
    });

    $("#login-submit-move").click(function(){
        login_move();
    });

    $("#regist-submit-move").click(function(){
        regist_move();
    });

    $("#login-submit").click(function(){
        login();
    });

    $("#regist-submit").click(function(){
        regist();
    });
});



