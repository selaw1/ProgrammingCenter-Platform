$(document).ready(function () {



    //To get example code back
    function refresh() {

        //Preparing a simple web program example
        language['HTML'] = '<!--HTML-->\n\n<!DOCTYPE html>\n<html>\n<body>\n\n<p id="demo_p">Click the button to change my color :)</p>\n\n<button id="demo_b">Click Me!</button>\n\n</body>\n</html>';
        language['CSS'] = '/*CSS*/\n\nbody{\n    text-align: center;\n}\n\np{\n    color:blue;\n    margin-top:150px;\n}';
        language['JAVASCRIPT'] = '//JAVASCRIPT\n\ndocument.getElementById("demo_b").addEventListener("click", function(){\n   let p = document.getElementById("demo_p");\n    p.style.color = "red";\n});';

        editor1.setValue(language['HTML'], -1);
        editor2.setValue(language['CSS'], -1);
        editor3.setValue(language['JAVASCRIPT'], -1);
    }


    //To run the code
    function compile() {

        document.body.onkeyup = function () {
            let html = editor1.getValue();
            let css = editor2.getValue();
            let js = editor3.getValue();
            let code = document.getElementById("code").contentWindow.document;

            code.open();
            code.writeln(html + "<style>" + css + "</style>" + "<script>" + js + "</script>");
            code.close();
        };

    };


    //Preparing the editors
    let language = {}
    language['HTML'] = '<!DOCTYPE html>\n\n<html>\n<head></head>\n\n<body>\n\n</body>\n</html>';
    language['CSS'] = '/*CSS*/';
    language['JAVASCRIPT'] = '//JAVASCRIPT';


    const editor1 = ace.edit("editor1");
    const editor2 = ace.edit("editor2");
    const editor3 = ace.edit("editor3");

    //To set the example HTML code / theme to dawn theme / mode to HTML / font size to 16
    editor1.setTheme("ace/theme/dawn");
    editor1.session.setMode("ace/mode/html");
    editor1.setFontSize(16);
    editor1.setValue(language['HTML'], -1);

    //To set the example CSS code / theme to dawn theme / mode to CSS / font size to 16
    editor2.setTheme("ace/theme/dawn");
    editor2.session.setMode("ace/mode/css");
    editor2.setFontSize(16);
    editor2.setValue(language['CSS'], -1);

    //To set the example JS code / theme to dawn / mode to JavaScript / font size to 16 
    editor3.setTheme("ace/theme/dawn");
    editor3.session.setMode("ace/mode/javascript");
    editor3.setFontSize(16);
    editor3.setValue(language['JAVASCRIPT'], -1);


    //When changing the fontsize for HTML editor
    $("#fontsize-html").change(function () {
        fontsize = $('#fontsize-html').val()
        editor1.setFontSize(parseInt(fontsize));
    });

    //When changing the fontsize for CSS editor
    $("#fontsize-css").change(function () {
        fontsize = $('#fontsize-css').val()
        editor2.setFontSize(parseInt(fontsize));
    });

    //When changing the fontsize for JS editor
    $("#fontsize-js").change(function () {
        fontsize = $('#fontsize-js').val()
        editor3.setFontSize(parseInt(fontsize));
    });


    //When changing the theme for HTML editor
    $("#theme-html").change(function () {
        themeSelected = $("#theme-html").val();
        if (themeSelected == "Dawn") {
            editor1.setTheme("ace/theme/dawn");
        } else if (themeSelected == "Solarized Light") {
            editor1.setTheme("ace/theme/solarized_light");
        } else if (themeSelected == "Twilight") {
            editor1.setTheme("ace/theme/twilight");
        } else if (themeSelected == "Chaos") {
            editor1.setTheme("ace/theme/chaos");
        } else if (themeSelected == "Clouds") {
            editor1.setTheme("ace/theme/clouds");
        } else if (themeSelected == "XCode") {
            editor1.setTheme("ace/theme/xcode");
        } else if (themeSelected == "Tomorrow Night") {
            editor1.setTheme("ace/theme/tomorrow_night");
        } else if (themeSelected == "Github") {
            editor1.setTheme("ace/theme/github");
        } else if (themeSelected == "Tomorrow Night Bright") {
            editor1.setTheme("ace/theme/tomorrow_night_bright");
        } else if (themeSelected == "Tomorrow Night Blue") {
            editor1.setTheme("ace/theme/tomorrow_night_blue");
        }
    });

    //When changing the theme for CSS editor
    $("#theme-css").change(function () {
        themeSelected = $("#theme-css").val();
        if (themeSelected == "Dawn") {
            editor2.setTheme("ace/theme/dawn");
        } else if (themeSelected == "Solarized Light") {
            editor2.setTheme("ace/theme/solarized_light");
        } else if (themeSelected == "Twilight") {
            editor2.setTheme("ace/theme/twilight");
        } else if (themeSelected == "Chaos") {
            editor2.setTheme("ace/theme/chaos");
        } else if (themeSelected == "Clouds") {
            editor2.setTheme("ace/theme/clouds");
        } else if (themeSelected == "XCode") {
            editor2.setTheme("ace/theme/xcode");
        } else if (themeSelected == "Tomorrow Night") {
            editor2.setTheme("ace/theme/tomorrow_night");
        } else if (themeSelected == "Github") {
            editor2.setTheme("ace/theme/github");
        } else if (themeSelected == "Tomorrow Night Bright") {
            editor2.setTheme("ace/theme/tomorrow_night_bright");
        } else if (themeSelected == "Tomorrow Night Blue") {
            editor2.setTheme("ace/theme/tomorrow_night_blue");
        }
    });

    //When changing the theme for JS editor
    $("#theme-js").change(function () {
        themeSelected = $("#theme-js").val();
        if (themeSelected == "Dawn") {
            editor3.setTheme("ace/theme/dawn");
        } else if (themeSelected == "Solarized Light") {
            editor3.setTheme("ace/theme/solarized_light");
        } else if (themeSelected == "Twilight") {
            editor3.setTheme("ace/theme/twilight");
        } else if (themeSelected == "Chaos") {
            editor3.setTheme("ace/theme/chaos");
        } else if (themeSelected == "Clouds") {
            editor3.setTheme("ace/theme/clouds");
        } else if (themeSelected == "XCode") {
            editor3.setTheme("ace/theme/xcode");
        } else if (themeSelected == "Tomorrow Night") {
            editor3.setTheme("ace/theme/tomorrow_night");
        } else if (themeSelected == "Github") {
            editor3.setTheme("ace/theme/github");
        } else if (themeSelected == "Tomorrow Night Bright") {
            editor3.setTheme("ace/theme/tomorrow_night_bright");
        } else if (themeSelected == "Tomorrow Night Blue") {
            editor3.setTheme("ace/theme/tomorrow_night_blue");
        }
    });


    document.getElementById('refresh').addEventListener("click", refresh);
    compile();


});