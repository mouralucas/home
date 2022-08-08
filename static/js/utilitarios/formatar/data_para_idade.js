// função para formatar data no padrão 2020-03-27 para idade em inteiro
function formatarDataParaIdade(aniversario) {
    if (aniversario.toString().indexOf('-') > -1) {
        let nascimento = aniversario.split("-");
        let dataNascimento = new Date(parseInt(nascimento[0], 10), parseInt(nascimento[1], 10) - 1, parseInt(nascimento[2], 10));

        let diferenca = Date.now() - dataNascimento.getTime();
        let idade = new Date(diferenca); // miliseconds from epoch
        return Math.abs(idade.getUTCFullYear() - 1970);
    } else {
        return aniversario;
    }
}