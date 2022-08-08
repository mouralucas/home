// função para formatar nome jose sant zam > Jose Sant Zam
function title(text) {
    if(text){
        var words = text.toLowerCase().trim().split(" ");
        for (var a = 0; a < words.length; a++) {
            var w = words[a];
            if(w[0])
                words[a] = w[0].toUpperCase() + w.slice(1);
        }
        return words.join(" ");
    }
}

function title_apenas_1_e_2_nome(text) {
    if(parseInt(text).toString() === "NaN" || parseInt(text).toString() === "undefined"){
        let words = text.toLowerCase().trim().split(" ");
        for (var a = 0; a < words.length; a++) {
            let w = words[a];
            if(w[0])
                words[a] = w[0].toUpperCase() + w.slice(1);
        }
        if(words[0] && words[words.length-1])
            text = words[0]+" "+words[words.length-1];
        else
            text = words.join(" ");
        return text;
    }
}