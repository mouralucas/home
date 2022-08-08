function printer(DOMExport){
    var w = window.open('', 'Print', 'height=1,width=1');
    w.document.write(document.head.innerHTML);
    w.document.write('<body>');
    w.document.write(DOMExport.innerHTML);
    w.document.write('</body>');
    w.document.write('</html>');
    setTimeout(function(){
        w.print();
        w.close();
    },200);
}

