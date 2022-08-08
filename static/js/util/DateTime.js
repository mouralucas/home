function formatDateTime(data, is_hr) {
    "use strict";
    var date = new Date();
    var timeOffset = date.getTimezoneOffset() / 60;

    if (data && data.substring) {
        let ano = data.substring(0, 4);
        let mes = data.substring(5, 7);
        let dia = data.substring(8, 10);
        let hora = data.substring(11, 13) !== '' ? data.substring(11, 13) : 0;
        let minuto = data.substring(14, 16) !== '' ? data.substring(14, 16) : 0;

        let nova_data;
        if (hora === 0 || minuto === 0) {
            nova_data = new Date(parseInt(ano), parseInt(mes) - 1, parseInt(dia));
        } else {
            nova_data = new Date(parseInt(ano), parseInt(mes) - 1, parseInt(dia), parseInt(hora) - timeOffset, parseInt(minuto));
        }

        let nova_data_dia = nova_data.getDate().toString().length === 1 ? '0' + nova_data.getDate().toString() : nova_data.getDate().toString();
        let nova_data_mes = (nova_data.getMonth() + 1).toString().length === 1 ? '0' + (nova_data.getMonth() + 1).toString() : (nova_data.getMonth() + 1).toString();
        let nova_data_ano = nova_data.getFullYear().toString().length === 1 ? '0' + nova_data.getFullYear().toString() : nova_data.getFullYear().toString();
        let nova_data_horas = nova_data.getHours().toString().length === 1 ? '0' + nova_data.getHours().toString() : nova_data.getHours().toString();
        let nova_data_minutos = nova_data.getMinutes().toString().length === 1 ? '0' + nova_data.getMinutes().toString() : nova_data.getMinutes().toString();


        if (!is_hr) {
            return nova_data_dia + '/' + nova_data_mes + '/' + nova_data_ano + ' às ' + nova_data_horas + ":" + nova_data_minutos;
        } else if (is_hr === "hora") {
            return nova_data_horas + ":" + nova_data_minutos;
        } else if (is_hr === 'data') {
            return nova_data_dia + '/' + nova_data_mes + '/' + nova_data_ano;
        } else {
        }
    } else {
        return '';
    }
}