function leitor_codigo_barras(cod_type, stringIDTarget, callbackfunction){
    var app = Quagga.init(
        {"inputStream":{"type":"LiveStream",  "target": document.querySelector(stringIDTarget),"constraints":{"width":{"min":640},"height":{"min":480},"aspectRatio":{"min":1,"max":100},"facingMode":"environment"}},"locator":{"patchSize":"medium","halfSample":true},"numOfWorkers":2,"frequency":10,"decoder":{"readers":[{"format":cod_type,"config":{}}]},"locate":true}
        ,
        function(err) {
            if (err) {
                console.log(err);
                return
            }
            Quagga.start();
        });


    Quagga.onProcessed(function(result) {
        var drawingCtx = Quagga.canvas.ctx.overlay,
            drawingCanvas = Quagga.canvas.dom.overlay;
        if (result) {
            if (result.boxes) {
                drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
                result.boxes.filter(function (box) {
                    return box !== result.box;
                }).forEach(function (box) {
                    Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, drawingCtx, {color: "green", lineWidth: 2});
                });
            }

            if (result.box) {
                Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, drawingCtx, {color: "#00F", lineWidth: 2});
            }

            if (result.codeResult && result.codeResult.code) {
                Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, drawingCtx, {color: 'red', lineWidth: 3});
            }
        }
    });

    Quagga.onDetected(function(result) {
        let code = result.codeResult.code;
        callbackfunction(code);
        Quagga.stop();
    });
}