    
    let code = document.getElementsByClassName('language-python');

    if (code.length) {
        code = document.getElementsByClassName('language-python');
    }else{
        code = document.getElementsByClassName('language-java'); 
    }
    
    // adding Id to code
    code[0].setAttribute("id", "1");
    code[1].setAttribute("id", "2");
    code[2].setAttribute("id", "3");

    function copy1() {    
        const copyText = document.getElementById('1').textContent;
        const textArea = document.createElement('textarea');
        textArea.textContent = copyText;
        document.body.append(textArea);
        textArea.select();
        document.execCommand("copy");
        textArea.remove();
        alert("The Following Code Has Been Copied\n\n"+ copyText +"\nDon't forget to change the language in the compiler!")
    }

    function copy2() {
        const copyText = document.getElementById('2').textContent;
        const textArea = document.createElement('textarea');
        textArea.textContent = copyText;
        document.body.append(textArea);
        textArea.select();
        document.execCommand("copy");
        textArea.remove();
        alert("The Following Code Has Been Copied\n\n"+ copyText +"\nDon't forget to change the language in the compiler!")
    }

    function copy3() {
        const copyText = document.getElementById('3').textContent;
        const textArea = document.createElement('textarea');
        textArea.textContent = copyText;
        document.body.append(textArea);
        textArea.select();
        document.execCommand("copy");
        textArea.remove();
        alert("The Following Code Has Been Copied\n\n"+ copyText +"\nDon't forget to change the language in the compiler!")
    }

    document.getElementById('button2').addEventListener('click', copy1);
    document.getElementById('button3').addEventListener('click', copy2);
    document.getElementById('button4').addEventListener('click', copy3);
