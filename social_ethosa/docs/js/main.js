var showed = 1;
var language = "en";
function toggle(){
    if (showed == 1){
        $(".menu").animate({width: "0%"});
        $("#toggler").css({transform: "90deg"});
        $("#MainMenu").animate({left: "1%"});
        $(".menu").css({position: "absolute"});
        $(".menu").css({display: "none"});
        showed = 0;
    } else {
        $(".menu").animate({width: "22%"});
        $("#MainMenu").animate({left: "23%"});
        $("#toggler").css({transform: "0deg"});
        $(".menu").css({position: "fixed"});
        $(".menu").css({display: "block"});
        showed = 1;
    }
}

function showImage(image, path){
    $(".imageViewerBack").css({display : "inline-block"});
    $(image).attr("src", path);
    $(".imageViewer").css({backgroundImage: "url("+path+")"});
    $(".imageViewer").css({backgroundSize: "100%"});
}

function hideImage(){
    $(".imageViewerBack").css({display : "none"});
}

function changeLanguage(){
    if (language == "en"){
        language = "ru";
        $("body").css({fontFamily: "Segoe UI Light, sans-serif"});
        $("body").css({fontWeight: "300"});
        $("#head").text("Привет, Social-ethosa!");
        $("#changeButton").text("Сменить язык");
        $("#contentMenu").text("Меню");
        $("#start").text("Библиотека для Python, использующая requests");
        $("#getstart").text("Начало работы");
        $("#installing").text("Установка:");
        $("#import").text("Импорт библиотеки:");
        $("#fileUploader").text("Использование загрузчика файлов:");
        $("#vkcom1").html($("#vkcom1").html().replace("the group_id parameter should be used if you are going to log in through a group.",
                                            "параметр group_id следует использовать, если вы собираетесь войти через группу."));
        $("#vkcom1").html($("#vkcom1").html().replace("In this example, we will use group authorization.",
                                            "В этом примере мы будем использовать авторизацию через группу."));
    } else {
        language = "en";
        $("body").css({fontFamily: "'Raleway', sans-serif"});
        $("body").css({fontWeight: "600"});
        $("#head").text("Hello, social-ethosa!");
        $("#changeButton").text("Change language");
        $("#contentMenu").text("Menu");
        $("#start").text("A Python library that uses requests");
        $("#getstart").text("Get started");
        $("#installing").text("Installation:");
        $("#import").text("Import:");
        $("#fileUploader").text("using the file Uploader:");
        $("#vkcom1").html($("#vkcom1").html().replace("параметр group_id следует использовать, если вы собираетесь войти через группу.",
                                    "the group_id parameter should be used if you are going to log in through a group."));
        $("#vkcom1").html($("#vkcom1").html().replace("В этом примере мы будем использовать авторизацию через группу.",
                                            "In this example, we will use group authorization."));
    }
}