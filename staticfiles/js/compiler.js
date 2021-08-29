$(document).ready(function () {




    //To run the code and get all the status
    function runCode() {
        if (ongoing == true)
            return;
        ongoing = true;
        updateContent();
        $(".outputbox").hide();
        $("#runcode").prop('disabled', true);

        let token = $(":input[name='csrfmiddlewaretoken']").val();
        let input_given = $("#custom-input").val();
        let run_data = {
            source: source_code,
            lang: selectedLang,
            csrfmiddlewaretoken: token
        };
        if ($("#user-input").prop('checked') == true) {
            run_data.input = input_given;
        }


        // AJAX request to Django for running code
        $.ajax({
            url: "run/",
            type: "POST",
            data: run_data,
            dataType: "json",
            timeout: 1000000,
            success: function (response) {
                ongoing = false;
                $("html, body").delay(150).animate({
                    scrollTop: $('#showers').offset().top
                }, 1000);
                $(".outputbox").show();
                $("#runcode").prop('disabled', false);

                let cstat = response.compile_status;
                let rstat = response.run_status.status;

                if (cstat == "OK") {
                    $(".compilestat").children(".value").html(response.compile_status);
                    $(".runstat").children(".value").html(response.run_status.status);
                    $(".time").children(".value").html(response.run_status.time_used);
                    $(".memory").children(".value").html(response.run_status.memory_used);

                    if (rstat == "AC") {

                        $(".outputerror").hide();
                        $(".io-show").show();
                        $(".outputo").html(response.run_status.output_html).css("color", "#fff");;

                        if ($("#user-input").prop('checked') == true)
                            $(".outputi").html(input_given).css("color", "#fff");
                        else
                            $(".outputi").html("Standard input is empty").css("color", "#eee");

                    } else {
                        $(".io-show").show();
                        $(".outputo").html("Standard output is empty").css("color", "#eee");
                        if ($("#user-input").prop('checked') == true)
                            $(".outputi").html(input_given).css("color", "#fff");
                        else
                            $(".outputi").html("Standard input is empty").css("color", "#a6a6a6");
                        $(".outputerror").show();

                        if (rstat == "MLE") {
                            $(".errorkey").html("Memory Error");
                            $(".errormessage").html("Memory limit exceeded");
                        } else if (rstat == "TLE") {
                            $(".errorkey").html("Timeout Error");
                            $(".errormessage").html("Time limit exceeded.");
                        } else {
                            $(".errorkey").html("Runtime Error");
                            $(".errormessage").html(response.run_status.status_detail);
                        }
                    }
                } else {
                    $(".io-show").show();
                    $(".outputo").html("Standard output is empty").css("color", "#eee");
                    if ($("#user-input").prop('checked') == true)
                        $(".outputi").html(input_given).css("color", "#fff");
                    else
                        $(".outputi").html("Standard input is empty").css("color", "#a6a6a6");
                    $(".time").children(".value").html("0.0");
                    $(".memory").children(".value").html("0");
                    $(".compilestat").children(".value").html("N/A");
                    $(".runstat").children(".value").html("CE");

                    $(".outputerror").show();
                    $(".errorkey").html("Compile Error");
                    $(".errormessage").html(response.compile_status);

                }
            },

            error: function (error) {

                ongoing = false;
                $("html, body").delay(150).animate({
                    scrollTop: $('#showers').offset().top
                }, 1000);

                $("#runcode").prop('disabled', false);
                $(".outputbox").show();
                $(".io-show").show();
                $(".outputo").html("Standard output is empty").css("color", "#eee");
                if ($("#user-input").prop('checked') == true)
                    $(".outputi").html(input_given).css("color", "#fff");
                else
                    $(".outputi").html("Standard input is empty").css("color", "#eee");
                $(".outputio").show();
                $(".time").children(".value").html("0.0");
                $(".memory").children(".value").html("0");
                $(".compilestat").children(".value").html("N/A");
                $(".runstat").children(".value").html("N/A");

                $(".errorkey").html("Server error");
                $(".errormessage").html("Bad Request(403). Please try again!");


            }
        });
    }


    //To get the current contents in the editor
    function updateContent() {
        source_code = editor.getValue();
    }


    //To Download the code in the editor
    function download(content, lang) {
        let e = {
            "C": "c",
            "CPP": "cpp",
            "CSHARP": "cs",
            "GO": "go",
            "JAVA": "java",
            "JAVASCRIPT": "js",
            "KOTLIN": "kt",
            "PHP": "php",
            "PYTHON3": "py",
            "RUBY": "rb",
            "R": "r",
            "SWIFT": "swift",
        };

        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
        element.setAttribute('download', "source_code." + e[lang]);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }


    // Example codes 
    function helloWorldCode() {
        if (selectedLang == 'PYTHON3') {
            language['PYTHON3'] = "print ('Hello World!')\n";
        } else if (selectedLang == 'PHP') {
            language['PHP'] = '<?php\n echo "Hello World";\n?>';
        } else if (selectedLang == 'CPP') {
            language['CPP'] = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n     cout << "Hello World!" << endl;\n     return 0;\n}\n';
        } else if (selectedLang == 'CSHARP') {
            language['CSHARP'] = 'using System;\n\nnamespace MyApplication\n{\n  class Program\n  {\n    static void Main(string[] args)\n    {\n      System.Console.WriteLine("Hello World!");\n    }\n  }\n}';
        } else if (selectedLang == 'GO') {
            language['GO'] = 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello World")\n}\n';
        } else if (selectedLang == 'JAVA') {
            language['JAVA'] = 'class TestClass {\n    public static void main(String args[] ) throws Exception {\n        System.out.println("Hello World!");\n    }\n}\n';
        } else if (selectedLang == 'KOTLIN') {
            language['KOTLIN'] = 'fun main(args: Array<String>) {\n println("Hello, world!")\n}';
        }else if (selectedLang == 'RUBY') {
            language['RUBY'] = "print 'Hello World!'\n";
        }else if (selectedLang == 'R') {
            language['R'] = 'cat("Hello World")\n';
        }else if (selectedLang == 'SWIFT') {
            language['SWIFT'] = 'import Swift\n\nprint("Hello, World!")\n';
        }

        editor.setValue(language[selectedLang], -1);
    }

    function arrayCode() {
        if (selectedLang == 'PYTHON3') {
            language['PYTHON3'] = 'thislist = ["apple", "banana", "cherry"]\nprint(thislist)';
        } else if (selectedLang == 'PHP') {
            language['PHP'] = '<?php\n$cars = array("Volvo", "BMW", "Toyota");\n echo "I like " . $cars[0] . ", " . $cars[1] . " and " . $cars[2] . ".";\n?>';
        } else if (selectedLang == 'CPP') {
            language['CPP'] = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n  string cars[4] = {"Volvo", "BMW", "Ford", "Mazda"};\n  cout << cars[0];\n  return 0;\n}';
        } else if (selectedLang == 'CSHARP') {
            language['CSHARP'] = 'using System;\n\nnamespace MyApplication\n{\n  class Program\n  {\n    static void Main(string[] args)\n    {\n      string[] cars = {"Volvo", "BMW", "Ford", "Mazda"};\n      Console.WriteLine(cars[0]);\n    }\n  }\n}';
        } else if (selectedLang == 'GO') {
            language['GO'] = 'package main\n\nimport "fmt"\n\nfunc main() {\n    b := [5]int{1, 2, 3, 4, 5}\n    fmt.Println("array:", b)\n}\n';
        } else if (selectedLang == 'JAVA') {
            language['JAVA'] = 'class TestClass {\n    public static void main(String args[] ) throws Exception {\n        String[] cars = {"Volvo", "BMW", "Ford", "Mazda"};\n        System.out.println(cars[0]);\n    }\n}\n';
        } else if (selectedLang == 'KOTLIN') {
            language['KOTLIN'] = 'fun main(args: Array<String>) {\n    val num = Array(5, {i-> i*1})\n    for (i in 0..num.size-1)\n    {\n        println(num[i])\n    }\n}';
        }else if (selectedLang == 'RUBY') {
            language['RUBY'] = "ary = [1, 'two', 3.0]\nprint(ary[1])\n";
        }else if (selectedLang == 'R') {
            language['R'] = 'thisarray <- c(1:5)\nthisarray';
        }else if (selectedLang == 'SWIFT') {
            language['SWIFT'] = 'import Swift\n\nlet oddNumbers = [1, 3, 5, 7, 9, 11, 13, 15]\nprint(oddNumbers)';
        }

        editor.setValue(language[selectedLang], -1);
    }

    function ifCode() {
        if (selectedLang == 'PYTHON3') {
            language['PYTHON3'] = 'a = 33\nb = 200\n\nif b > a:\n    print("b is greater than a")';
        } else if (selectedLang == 'PHP') {
            language['PHP'] = '<?php\n$t = 19;\n\nif ($t < 20) {\n    echo "Have a good day!";\n}\n?>';
        }else if (selectedLang == 'CPP') {
            language['CPP'] = '#include <iostream>\nusing namespace std;\n\nint main() {\n    if (20 > 18) {\n    cout << "20 is greater than 18";\n    }\n    return 0;\n}';
        }else if (selectedLang == 'KOTLIN'){
            language['KOTLIN'] = 'fun main(args: Array<String>) {\n    val number = -10\n    if (number > 0) {\n        print("Positive number")\n    } else {\n        print("Negative number")\n    }\n}';
        } else if (selectedLang == 'CSHARP') {
            language['CSHARP'] = 'using System;\n\nnamespace MyApplication\n{\n  class Program\n  {\n    static void Main(string[] args)\n    {\n        if (20 > 18) {\n          Console.WriteLine("20 is greater than 18");\n        }\n    }\n  }\n}';
        } else if (selectedLang == 'GO') {
            language['GO'] = 'package main\n\nimport "fmt"\n\nfunc main() {\n    if 7%2 == 0 {\n        fmt.Println("7 is even")\n    } else {\n        fmt.Println("7 is odd")\n    }\n}';
        } else if (selectedLang == 'JAVA') {
            language['JAVA'] = 'class TestClass {\n    public static void main(String args[] ) throws Exception {\n        if (20 > 18) {\n            System.out.println("20 is greater than 18");\n        }\n    }\n}\n';
        }else if (selectedLang == 'RUBY') {
            language['RUBY'] = 'x = 1\nif x > 2\n    puts "x is greater than 2"\nelse\n    puts "x is less than 2"\nend';
        }else if (selectedLang == 'R') {
            language['R'] = 'a <- 33\nb <- 200\n\nif (b > a) {\n    print("b is greater than a")\n}';
        }else if (selectedLang == 'SWIFT') {
            language['SWIFT'] = 'import Swift\n\nlet number = 10\nif number > 0 {\n    print("Number is positive.")\n}\nprint("This statement is always executed.")';
        }
        editor.setValue(language[selectedLang], -1);
    }

    function forLoopCode() {
        if (selectedLang == 'PYTHON3') {
            language['PYTHON3'] = 'for x in range(6):\n    print(x)';
        } else if (selectedLang == 'PHP') {
            language['PHP'] = '<?php\nfor ($x = 0; $x <= 10; $x++) {\n    echo "The number is: $x <br>";\n}\n?>';
        }else if (selectedLang == 'CPP') {
            language['CPP'] = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n  for (int i = 0; i < 7; i++) {\n    cout << i << "\\n";\n}\n  return 0;\n}';
        }else if (selectedLang == 'KOTLIN'){
            language['KOTLIN'] = 'fun main(args: Array<String>) {\n    val num = Array(5, {i-> i*1})\n    for (i in 0..num.size-1)\n    {\n        println(num[i])\n    }\n}';
        } else if (selectedLang == 'CSHARP') {
            language['CSHARP'] = 'using System;\n\nnamespace MyApplication\n{\n  class Program\n  {\n    static void Main(string[] args)\n    {\n        for (int i = 0; i < 5; i++) {\n          Console.WriteLine(i);\n        }\n    }\n  }\n}';
        } else if (selectedLang == 'GO') {
            language['GO'] = 'package main\n\nimport "fmt"\n\nfunc main() {\n    sum := 0\n    for i := 1; i < 5; i++ {\n        sum += i\n    }\n    fmt.Println(sum)\n}';
        } else if (selectedLang == 'JAVA') {
            language['JAVA'] = 'class TestClass {\n    public static void main(String args[] ) throws Exception {\n        for (int i = 0; i < 5; i++) {\n            System.out.println(i);\n        }\n    }\n}\n';
        }else if (selectedLang == 'RUBY') {
            language['RUBY'] = 'for i in 0..5\n    puts "Value of local variable is #{i}"\nend'
        }else if (selectedLang == 'R') {
            language['R'] = 'for (x in 1:10) {\n    print(x)\n}';
        }else if (selectedLang == 'SWIFT') {
            language['SWIFT'] = 'import Swift\n\nfor i in 1...10 {\n    print(i)\n}';
        }
        editor.setValue(language[selectedLang], -1);
    }



    //Preparing the Hello World program 
    let language = {}
    language['CPP'] = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n     cout << "Hello World!" << endl;\n     return 0;\n}\n';
    language['PYTHON3'] = "print ('Hello World!')\n";
    language['PHP'] = '<?php\n echo "Hello World";\n?>';
    language['CPP'] = '#include <iostream>\nusing namespace std;\n\nint main()\n{\n     cout << "Hello World!" << endl;\n     return 0;\n}\n';
    language['CSHARP'] = 'using System;\n\nnamespace MyApplication\n{\n  class Program\n  {\n    static void Main(string[] args)\n    {\n      System.Console.WriteLine("Hello World!");\n    }\n  }\n}';
    language['GO'] = 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello World")\n}\n';
    language['JAVA'] = 'class TestClass {\n    public static void main(String args[] ) throws Exception {\n        System.out.println("Hello World!");\n    }\n}\n';
    language['KOTLIN'] = 'fun main(args: Array<String>) {\n println("Hello, world!")\n}';
    language['RUBY'] = "print 'Hello World!'\n";
    language['R'] = 'cat("Hello World")\n';
    language['SWIFT'] = 'import Swift\n\nprint("Hello, World!")\n'

    //------From Ace Documentation on inserting the editor------//
    const editor = ace.edit("editor");
    let ongoing = false;
    editor.setOptions({
        "firstLineNumber": 0,
        'tabSize': 4,
        'fontSize': 20
    });

    //To set the theme to dawn theme / mode to c++
    editor.setTheme("ace/theme/dawn");
    editor.session.setMode("ace/mode/c_cpp");

    //To Show Hello World Program in C++
    let selectedLang = "CPP";
    editor.setValue(language[selectedLang], -1);

    let source_code = editor.getValue();

    //StatusBar
    let StatusBar = ace.require("ace/ext/statusbar").StatusBar;
    let statusBar = new StatusBar(editor, document.getElementById("editor-statusbar"));

    //To disable Run Code Button when editor is empty
    editor.getSession().on('change', function (e) {
        updateContent();
        if (source_code == "") {
            $("#runcode").prop('disabled', true);
            $('#runcode').prop('title', "Editor is Empty! Please write some code.");
        } else {
            $("#runcode").prop('disabled', false);
            $('#runcode').prop('title', "Compile and Run");
        }
    });
    editor.session.getSelection().clearSelection();


    //When changing the fontsize
    $("#fontsize").change(function () {
        fontsize = $('#fontsize').val()
        editor.setFontSize(parseInt(fontsize));
    });

    //When changing the theme
    $("#theme").change(function () {
        themeSelected = $("#theme").val();
        if (themeSelected == "Dawn") {
            editor.setTheme("ace/theme/dawn");
        } else if (themeSelected == "Solarized Light") {
            editor.setTheme("ace/theme/solarized_light");
        } else if (themeSelected == "Twilight") {
            editor.setTheme("ace/theme/twilight");
        } else if (themeSelected == "Chaos") {
            editor.setTheme("ace/theme/chaos");
        } else if (themeSelected == "Clouds") {
            editor.setTheme("ace/theme/clouds");
        } else if (themeSelected == "XCode") {
            editor.setTheme("ace/theme/xcode");
        } else if (themeSelected == "Tomorrow Night") {
            editor.setTheme("ace/theme/tomorrow_night");
        } else if (themeSelected == "Github") {
            editor.setTheme("ace/theme/github");
        } else if (themeSelected == "Tomorrow Night Bright") {
            editor.setTheme("ace/theme/tomorrow_night_bright");
        } else if (themeSelected == "Tomorrow Night Blue") {
            editor.setTheme("ace/theme/tomorrow_night_blue");
        }
    });

    // When Changing the language
    $("#lang").change(function () {
        selectedLang = $("#lang").val();
        editor.setValue(language[selectedLang], -1);

        if (selectedLang == "CPP") {
            editor.getSession().setMode("ace/mode/c_cpp");
        } else if (selectedLang == 'PYTHON3') {
            editor.getSession().setMode("ace/mode/python");
        }else if (selectedLang == 'GO') {
                editor.getSession().setMode("ace/mode/golang");
        } else {
            editor.getSession().setMode("ace/mode/" + selectedLang.toLowerCase());
        }
        editor.session.getSelection().clearSelection();
    });

    // When Changing the example code
    $('#exapmle-helloworld').click(helloWorldCode);
    $('#exapmle-array').click(arrayCode);
    $('#exapmle-for').click(forLoopCode);
    $('#exapmle-if').click(ifCode);

    //To show user input box
    $('#user-input').click(function () {
        $(".input-container").slideToggle();
    });

    // To download the code
    $("#download").click(function () {
        updateContent();
        download(source_code, $("#lang").val());

    });

    // To run the code
    $("#runcode").click(function () {
        runCode();
    });
});