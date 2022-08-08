// div do popup dos filtros
$(document.getElementsByClassName('main')[0]).append('<div id="popup"></div>');

// letiavel com dict de opções
let optionsDefaultTables = {
    allowColumnReordering: false,
    filterRow: {
        visible: false
    },
    headerFilter: {
        visible: true
    },
    export: {
        enabled: true,
    },
    grouping: {
        autoExpandAll: false,
        contextMenuEnabled: true,
        expandMode: "rowClick"
    },
    groupPanel: {
        visible: false,
        allowColumnDragging: false
    },
    filterPanel: {
        visible: false
    },
    onFileSaving: function (e) {
        "use strict";
        e.fileName = e.element[0].id;
    },
    filterBuilderPopup: {
        minWidth: 300,
        width: 'auto',
        height: 'auto',
        title: "Avançado",
        dragEnabled: true,
        resizeEnabled: true,
        shading: false,
        closeOnOutsideClick: false,
    },
    paging: {
        pageSize: 10,
    },
    pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [20, 50, 0],
        showNavigationButtons: true,
        showInfo: true
    },
    scrolling: false,
    onContentReady: function ReplaceHeaderClass(e) {
        "use strict";
        replaceHeader(e);

        setTimeout(function () {
            let el = e.component.element()[0].querySelector(".dx-page-size:last-child");
            if (el !== null) {
                if (el.innerHTML === "20") {
                    el.innerHTML = "20";
                    el.setAttribute('aria-label', "Display 20 items on page");
                    el.onclick = function () {
                        e.component.pageSize(20);
                    };
                }
                if (el.innerHTML === "50") {
                    el.innerHTML = "50";
                    el.setAttribute('aria-label', "Display 50 items on page");
                    el.onclick = function () {
                        e.component.pageSize(50);
                    };
                }
                if (el.innerHTML === "0") {
                    el.innerHTML = "Ler Tudo";
                    el.setAttribute('aria-label', "Display Ler Tudo items on page");
                    el.onclick = function () {
                        e.component.pageSize(0);
                    };
                }
            }
        }, 100);

        if (e.component.element()[0].querySelector(".dx-pages") !== null) {
            e.component.element()[0].querySelector(".dx-pages").style.visibility = "visible";
        }
        if (e.component._options._optionManager._options.paging.pageSize === 1) {
            e.component.pageSize(50);
        }

        if (e.component._options._optionManager._options.paging.pageSize === 2) {
            e.component.pageSize(0);
        }

        $('[data-toggle="tooltip"]').tooltip();
    },
    rowAlternationEnabled: true,
    searchPanel: {
        visible: true,
        highlightCaseSensitive: true,
        placeholder: ""
    },
    selection: {
        mode: "single"
    },
    sorting: {
        mode: "multiple"
    },
    allowColumnResizing: true,
    columnAutoWidth: true,
    showColumnLines: true,

    showRowLines: true,
    columnChooser: {
        enabled: true
    },
    columnFixing: {
        enabled: true
    },
};

// Função para converter um decimal, obs: receber parâmetro inteiro 2 para deixar formatado exemplo: 2.000.000,00
Number.prototype.toLocaleFixed = function (n) {
    if (typeof parseFloat(this) === 'number') {
        return parseFloat(this).toLocaleString('pt-BR', {
            minimumFractionDigits: n,
            maximumFractionDigits: n
        });
    } else {
        return this;
    }
};

// default da para costumizar a tabela, tem que ter em todas as tables
function btnAfterEnd(e) {
    e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].setAttribute('end', 'true');
    if (e.component._$element[0].getElementsByClassName('dx-icon-filter-advanced').length === 0 && e.component._$element[0].getElementsByClassName('dx-icon-clear-filter').length === 0) {
        e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].classList.remove('mr-2');
        e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].classList.remove('ml-2');
    }
    if (e.component._$element[0].getElementsByClassName('dx-toolbar-before')[0].children.length === 0) {
        if (e.component._$element[0].getElementsByClassName('dx-datagrid-header-panel')[0] !== undefined) {
            e.component._$element[0].getElementsByClassName('dx-datagrid-header-panel')[0].style.display = 'none';
            e.component._$element[0].getElementsByClassName('searchRow')[0].classList.add('mb-2');
        }
        if (e.component._$element[0].getElementsByClassName('dx-treelist-header-panel')[0] !== undefined) {
            e.component._$element[0].getElementsByClassName('dx-treelist-header-panel')[0].style.display = 'none';
            e.component._$element[0].getElementsByClassName('searchRow')[0].classList.add('mb-2');
        }
    }
}

function btnFilterAdvanced(e) {
    if (e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].getAttribute('end') !== "true") {
        if (e.component._$element[0].getElementsByClassName('dx-icon-filter-advanced').length === 0) {
            let mx_w700px = window.matchMedia("(max-width: 700px)");
            let float;
            let widthPopup;
            if (mx_w700px.matches) {
                widthPopup = 250;
                float = 'left';
            } else {
                widthPopup = 400;
                float = 'right';
            }
            let divBtnFilterAdvanced = $("<a/>").addClass('cursor-pointer btn btn-tabelas d-flex align-items-center ml-1')
                .attr('data-toggle', 'tooltip').attr('data-placement', 'top').attr('data-title', 'Filtro Avançado')
                .click(function () {
                    e.component.option("filterBuilderPopup", {
                        minWidth: widthPopup,
                        width: 'auto',
                        height: 'auto',
                        minHeight: 240,
                        title: "Filtro Avançado",
                        dragEnabled: true,
                        resizeEnabled: true,
                        shading: false,
                        closeOnOutsideClick: false,
                        visible: true
                    });
                });
            $("<i/>").addClass('icon_menu01').css('font-size', '1.3rem').appendTo(divBtnFilterAdvanced.appendTo(e.component._$element[0].getElementsByClassName('seletordivFilterAdvancedAndClearFilters')[0]));
        }
    }
}

function btnRefreshTable(e, response) {
    if (e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].getAttribute('end') !== "true") {
        if (e.component._$element[0].getElementsByClassName('icon_update').length === 0) {
            let btnUpdate = $("<a/>").addClass('cursor-pointer btn btn-tabelas d-flex align-items-center ml-1')
                .attr('data-toggle', 'tooltip').attr('data-placement', 'top').attr('data-title', 'Atualizar')
                .click(function () {
                    response.ajax();
                });
            $("<i/>").addClass('icon_update').css('font-size', '1.3rem').appendTo(btnUpdate.appendTo(e.component._$element[0].getElementsByClassName('seletordivFilterAdvancedAndClearFilters')[0]));
        }
    }
}

function btnClearFilter(e) {
    if (e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].getAttribute('end') !== "true") {
        if (e.component._$element[0].getElementsByClassName('icon_broom').length === 0) {
            let divBtnFilterClear = $("<a/>").addClass('btn btn-tabelas d-flex align-items-center ml-1')
                .attr('data-toggle', 'tooltip').attr('data-placement', 'top').attr('data-title', 'Limpar todos os filtros')
                .click(function () {
                    e.component.clearFilter();
                    for (let i = 0; i < e.element[0].getElementsByClassName('seletorSpanFilter ').length; i++) {
                        e.element[0].getElementsByClassName('seletorSpanFilter ')[i].setAttribute('data-value', '');
                        e.element[0].getElementsByClassName('seletorSpanFilter ')[i].setAttribute('data-between', '');
                        e.element[0].getElementsByClassName('seletorSpanFilter ')[i].setAttribute('data-expression', '');
                        e.element[0].getElementsByClassName('seletorSpanFilter ')[i].classList.remove('text-primary');
                    }
                });
            $("<i/>").addClass('icon_broom').css('font-size', '1.3rem').appendTo(divBtnFilterClear.appendTo(e.component._$element[0].getElementsByClassName('seletordivFilterAdvancedAndClearFilters')[0]));
        }
    }
}

// adiciona botão de exportar excel
function addBtnExport(e) {
    if (e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].getAttribute('end') !== "true") {
        let btnExport = $("<a/>").addClass('btn btn-tabelas d-flex align-items-center ml-1')
            .attr('data-toggle', 'tooltip').attr('data-placement', 'top').attr('data-title', 'Exportar Excel')
            .click(function () {
                e.component.exportToExcel();
            });
        $("<i/>").addClass('icon_export-xlsx').css('font-size', '1.3rem').appendTo(btnExport.appendTo($(e.element[0].getElementsByClassName('seletordivFilterAdvancedAndClearFilters')[0])));
    }
}

// adiciona botão de esconder colunas
function addBtnChooser(e) {
    if (e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].getAttribute('end') !== "true") {
        let btnChooser = $("<a/>").addClass('btn btn-tabelas d-flex align-items-center ml-1')
            .attr('data-toggle', 'tooltip').attr('data-placement', 'top').attr('data-title', 'Seletor de Colunas')
            .click(function () {
                e.component.showColumnChooser();
            });
        $("<i/>").addClass('icon_table-cell').css('font-size', '1.3rem').appendTo(btnChooser.appendTo($(e.element[0].getElementsByClassName('seletordivFilterAdvancedAndClearFilters')[0])));
    }
}

// função para costumização da barra de pesquisa e layout da tabela
function searchPanelCustomize(e) {
    if (e.parentType === 'searchPanel') {
        if (e.component._$element[0].getElementsByClassName('searchRow').length === 0) {
            let mx_w700px = window.matchMedia("(max-width: 700px)");
            let float;
            let widthPopup;
            if (mx_w700px.matches) {
                widthPopup = 250;
                float = 'left';
            } else {
                widthPopup = 400;
                float = 'right';
            }
            let divRow = $("<div/>").addClass('row d-flex searchRow mb-1 flex-wrap justify-content-between h-auto');
            let divColsSearch = $("<div/>").addClass('col-xl col-lg col-md-12 col-sm-12').appendTo(divRow);

            let divSearchMaisBtns = $("<div/>").addClass('d-flex mb-1').appendTo(divColsSearch);

            let divSearch = $("<div/>").addClass('input-group').appendTo(divSearchMaisBtns);

            let divLupa = $("<div/>").addClass('input-group-prepend').css('background-color', '').append($("<span/>").addClass('input-group-text dx-icon-search')).appendTo(divSearch);
            let searchInput = $(e.editorElement[0]).css('display', 'none').appendTo(divSearch);

            let divFilterAdvancedAndClearFilters = $("<div/>").addClass('d-flex seletordivFilterAdvancedAndClearFilters').appendTo(divSearchMaisBtns);

            let divColsToolbar = $("<div/>").addClass('d-flex align-items-center flex-wrap seletorColsSearch h-auto').css('text-align', float).appendTo(divRow);

            $(e.component._$element[0]).prepend(divRow);
        }
    }
}

// reset para btns do Header para costumizar
function resetGroupToolbar(e) {
    let btnGroupToolbar = e.element[0].getElementsByClassName('dx-toolbar-items-container')[0].getElementsByClassName('dx-toolbar-after')[0];
    e.element[0].getElementsByClassName('dx-toolbar-items-container')[0].getElementsByClassName('dx-toolbar-after')[0].innerHTML = '';
}

// função para criar botões genéricos na tabela
function btnGroupGeneric(e, arrayBtns) {
    if (e.component._$element[0].getElementsByClassName('seletorColsSearch')[0].getAttribute('end') !== "true") {

        let divBtnGeneric;
        let btnGeneric;
        if (arrayBtns.length > 0) {
            for (let c = 0; c < arrayBtns.length; c++) {
                divBtnGeneric = $("<div/>").addClass('mx-2 mb-1');
                // btn genérico
                for (let i = 0; i < arrayBtns[c].length; i++) {
                    btnGeneric = $("<a/>").addClass(arrayBtns[c][i].btnClass.toString() + ' mr-1 text-right ').attr('data-toggle', 'tooltip').attr('data-placement', 'top').attr('data-title', arrayBtns[c][i].btnTooltip.toString()).click(arrayBtns[c][i].btnClick);
                    btnGeneric.appendTo(divBtnGeneric);
                }
                divBtnGeneric.appendTo($(e.element[0].getElementsByClassName('seletorColsSearch')[0]));
            }
        }
    }
}

// função para repassar dar um float right nos filtros e um float left no texto nome da coluna
function replaceHeader() {
    $('.dx-header-filter').attr('data-toggle', 'tooltip')
        .attr('data-placement', 'top')
        .attr('data-title', 'Filtro por Seleção');
    // replace search-panel
    $('.dx-datagrid-search-panel, .dx-treelist-search-panel').addClass('form-control').off('click').on('click', function () {
        $(this).find('.form-control').focus();
    }).css('width', '').find('.dx-texteditor-input').css('border', '0').addClass('form-control').attr('placeholder', 'Pesquisar nesta tabela...').parent().find('.dx-icon-search').remove();
    $('.dx-datagrid-search-panel, .dx-treelist-search-panel').find('.dx-texteditor-buttons-container').remove();

    $('.dx-datagrid-search-panel, .dx-treelist-search-panel').css("display", "block");
    // column caption
    $(".dx-header-filter-indicator").addClass("font-weight-bold");
    $(".dx-datagrid-text-content")
        .removeClass("dx-text-content-alignment-left").removeClass('dx-text-content-alignment-right')
        .css("text-align", "center ")
        .addClass('ml-3');
    // filter & sort icon
    $(".dx-column-indicators").css("float", "right");
    $(".dx-sort").css("float", "right");
    // header cell text alignment
    $('[role="columnheader"]').css('text-align', 'center');
}

// formatar valor em % e valor R$
function formatarValor(qualFormatoString, value) {
    let valor;
    switch (qualFormatoString) {
        case "%":
            valor = parseFloat(value).toLocaleFixed(2) + "%";
            break;
        case "R$":
            valor = "R$ " + parseFloat(value).toLocaleFixed(2);
            break;
    }
    return valor;
}

// tratamento de dados da celula
function replaceCell(container, options, qualFormatoString, fontSizeString) {
    options.component._$element.find('.dx-scrollable-wrapper').css('width', '100%');
    options.component._$element.find('.dx-scrollable-container').css('overflow-x', 'auto');

    container.css('text-align', 'center');
    let dataField = options.column.dataField;
    let value = options.data[dataField];
    if (parseFloat(options.data[dataField]).toString() === "NaN") {
        value = options.data[dataField];
    } else {
        value = formatarValor(qualFormatoString, value);
    }
    if (fontSizeString === undefined) {
        fontSizeString = "";
    }
    if (qualFormatoString === "") {
        value = options.data[dataField];
    }
    if (options.data[dataField] === undefined || options.data[dataField] === null || options.data[dataField] === "null" || options.data[dataField] === "") {
        value = "";
    }
    container.html(`<p>
                      ${value}
                    </p>`).find("*").css('fontSize', fontSizeString);

}

//mascara de formatacao para miliar
function mascaraDeFormatacao3Digitos(valor) {
    let isNegativo = "";
    if (valor.substring(0, 1) === '-') {
        isNegativo = "-";
    }
    let value = valor.replace(/[^\d,]/g, '');
    let matches = /^(?:(?:(\d{1,3})?((?:\d{3})*)))((?:,\d*)?)$/.exec(value);
    if (!matches) {
        return;
    }
    let spaceified = matches[2].replace(/(\d{3})/g, '.$1');
    valor = [matches[1], spaceified, matches[3]].join('');
    return isNegativo + valor;
}

// formata o valor digitado pelo usuário 000.000.000,00 para o valor aceito pelo javascript 000 000 000 .00 separando . como casa decimal e sem separador de miliar
function formatarValorFiltro(dataType, value, itemExampleValue) {
    if (value !== "") {
        if (parseFloat(value).toString() === "NaN" && dataType === 'string') {
            // value = contentElement[0].getElementsByClassName('seletorInput')[0].value;
        } else {
            let whatFormat = itemExampleValue.substring(itemExampleValue.length - 3, itemExampleValue.length);
            if (whatFormat.indexOf(".") !== -1) {
                if (value.indexOf(",") !== -1) {
                    value = value.replace(/[.]/g, "x").replace(/[,]/g, ".").replace(/[x]/g, "");
                } else {
                    value = value.replace(/[.]/g, "");
                    value += '.00';
                }
            } else {
                // value = value;
            }
        }
    }
    return value;
}

// adicionando ícones para o select2 dentro do filtro condicional
function formatStat(state) {
    if (!state.id) {
        return state.text;
    }
    let className = "";

    switch (state.element.value.toLowerCase()) {
        case "contains":
            className = "dx-icon-contains";
            break;
        case "notcontains":
            className = "dx-icon-doesnotcontain";
            break;
        case "startswith":
            className = "dx-icon-startswith";
            break;
        case "endswith":
            className = "dx-icon-endswith";
            break;
        case "=":
            className = "dx-icon-equal";
            break;
        case "<>":
            className = "dx-icon-notequal";
            break;
        case "<":
            className = "dx-icon-less";
            break;
        case ">":
            className = "dx-icon-greater";
            break;
        case "<=":
            className = "dx-icon-lessorequal";
            break;
        case ">=":
            className = "dx-icon-greaterorequal";
            break;
        case "><":
            className = "dx-icon-range";
            break;
    }
    let $state = $(
        `<div class="small"><span class="${className} mr-2" style="font-size:1.2rem;"></span>${state.text}</div>`
    );
    return $state;
};

// funcao para verificar qual item do select2 foi selecionado
function optionsFilterChange(contentElement, option, currentExpression) {
    switch (option) {
        // executa para verificar qual foi selecionado no select
        case 'qual_selecionado':
            let selecionado = contentElement[0].getElementsByClassName('seletorFilter')[0].children[1].getElementsByClassName('select2-selection__rendered')[0].getAttribute('title');
            for (let i = 0; i < contentElement[0].getElementsByClassName('seletorFilter')[0].children[0].length; i++) {
                if (selecionado === contentElement[0].getElementsByClassName('seletorFilter')[0].children[0].children[i].textContent) {
                    let domSelect = contentElement[0].getElementsByClassName('seletorSelectFilter')[0].children[i].value;
                    if (domSelect === "><") {
                        contentElement[0].getElementsByClassName('seletorInputBetween')[0].style.display = 'block';
                        $(contentElement[0].getElementsByClassName('seletorInputBetweenPai')[0]).parent().find('.seletorInput').parent().removeClass('col-12').addClass('col-6')
                    } else {
                        contentElement[0].getElementsByClassName('seletorInputBetween')[0].style.display = 'none';
                        $(contentElement[0].getElementsByClassName('seletorInputBetweenPai')[0]).parent().find('.seletorInput').parent().removeClass('col-6').addClass('col-12')
                    }
                    return contentElement[0].getElementsByClassName('seletorFilter')[0].children[0].children[i].value;
                }
            }
            break;
        // funcao selecionar a expressao assim que o usuario reabrir o filtro caso tenha filtrado anteriormente ele vai carregar a expressao selecionada, pq todos os filtros usam o mesmo modal
        case 'selecione_expressao':
            for (let i = 0; i < contentElement[0].getElementsByClassName('seletorSelectFilter')[0].children.length; i++) {
                if (contentElement[0].getElementsByClassName('seletorSelectFilter')[0].children[i].value === currentExpression) {
                    contentElement[0].getElementsByClassName('seletorSelectFilter')[0].children[i].setAttribute('selected', "true");
                    if (currentExpression === "><") {
                        contentElement[0].getElementsByClassName('seletorInputBetween')[0].style.display = 'block';
                        $(contentElement[0].getElementsByClassName('seletorInputBetweenPai')[0]).parent().find('.seletorInput').parent().removeClass('col-12').addClass('col-6')
                    } else {
                        contentElement[0].getElementsByClassName('seletorInputBetween')[0].style.display = 'none';
                        $(contentElement[0].getElementsByClassName('seletorInputBetweenPai')[0]).parent().find('.seletorInput').parent().removeClass('col-6').addClass('col-12')
                    }
                }
            }
            break;
    }
}

// funcao que executa o modal de filtro cria o tamanho dele e chama as funcoes para carregar o modal com filtro anteriomente selecionado
let showInfo = function (dataField, data, dataType, _this, title, itemExampleValue) {
    let popup = null;
    let mx_w700px = window.matchMedia("(max-width: 700px)");
    let widthPopup;
    if (mx_w700px.matches) {
        widthPopup = 250;
    } else {
        widthPopup = 400;
    }
    let popupOptions = {
        // criando layout
        contentTemplate: function (contentElement) {
            let arrayOutrosFiltros = [];
            let colunas = _this.parent().parent().parent().children();
            for (let i = 0; i < colunas.length; i++) {
                if (colunas[i].getElementsByClassName('dx-column-indicators').length > 0) {
                    if (colunas[i].getElementsByClassName('dx-column-indicators')[0].getElementsByClassName('seletorSpanFilter').length > 0) {
                        let filtro = colunas[i].getElementsByClassName('dx-column-indicators')[0].getElementsByClassName('seletorSpanFilter')[0];
                        let filtro_expression = filtro.getAttribute('data-expression');
                        let filtro_value = filtro.getAttribute('data-value');
                        let filtro_value_betweeen = filtro.getAttribute('data-between');
                        let filtro_dataType = filtro.getAttribute('data-type');
                        let filtro_dataField = filtro.getAttribute('data-field');
                        let filtro_dataItem = filtro.getAttribute('data-item');

                        if (filtro_value !== "" && filtro_dataField !== dataField) {
                            filtro_value = formatarValorFiltro(filtro_dataType, filtro_value, filtro_dataItem);

                            if (filtro_expression === "><") {
                                if (filtro_value_betweeen.indexOf(",") !== -1) {
                                    filtro_value_betweeen = filtro_value_betweeen.replace(/[.]/g, "x").replace(/[,]/g, ".").replace(/[x]/g, "");
                                } else {
                                    filtro_value_betweeen = filtro_value_betweeen.replace(/[.]/g, "");
                                    filtro_value_betweeen += '.00';
                                }
                            }

                            if (filtro_expression !== "" && filtro_expression !== "><") {
                                arrayOutrosFiltros.push([filtro_dataField, filtro_expression, filtro_value]);
                            } else if (filtro_expression === "><") {
                                if (filtro_value < filtro_value_betweeen) {
                                    arrayOutrosFiltros.push([
                                        [filtro_dataField, ">", filtro_value],
                                        [filtro_dataField, "<", filtro_value_betweeen]
                                    ]);
                                } else {
                                    arrayOutrosFiltros.push([
                                        [filtro_dataField, "<", filtro_value],
                                        [filtro_dataField, ">", filtro_value_betweeen]
                                    ]);
                                }
                            }
                        }
                    }
                }
            }
            // select com condições
            let html = `
                    <div class="mt-2">
                        <div class="row">
                            <div class="col-12">
                                <fieldset class="seletorFilter form-group row m-auto">
                                    <select  class="seletorSelectFilter form-control select2-single">`;
            if (dataType === 'string') {
                html += `                <option value="contains">Contém</option>
                                        <option value="notcontains">Não Contém</option>
                                        <option value="startswith">Começa com</option>
                                        <option value="endswith">Termina com</option>`;
            }
            html += `                    <option value="=">Igual</option>
                                        <option value="<>">Diferente</option>`;
            if (dataType === 'string') {
            } else {
                html += `                <option value="<">Menor que</option>
                                        <option value=">">Maior que</option>
                                        <option value="<=">Menor que ou igual a</option>
                                        <option value=">=">Maior que ou igual a</option>
                                        <option value="><">Entre</option>
                                    `;
            }
            html += `
                                    </select>
                                </fieldset>
                            </div>
                        </div>
                        <div class="row mt-1">
                            <div class="col-12">
                                <input type="text" class="form-control seletorInput" value="${_this.attr('data-value')}">
                            </div>
                            <div  class="col-6 seletorInputBetweenPai">
                                <input style="display:none"  type="text" class="form-control seletorInputBetween" value="${_this.attr('data-between')}">
                            </div>
                        </div>
                    </div>
                    <hr class="mt-3">`;
            contentElement.append(html);

            optionsFilterChange(contentElement, 'selecione_expressao', _this.attr('data-expression'));

            $(contentElement[0].getElementsByClassName('seletorSelectFilter')[0]).on('change', function () {
                setTimeout(function () {
                    let ok = optionsFilterChange(contentElement, 'qual_selecionado', dataType);
                }, 100)
            });


            let div_footer = $("<div/>").addClass('d-flex justify-content-between align-items-center mt-3');


            let clear = $("<a/>").addClass('cursor-pointer text-danger small').html('Limpar Filtro').click(function () {
                arrayOutrosFiltros.push([dataField, 'contains', '']);
                data.filter(arrayOutrosFiltros);
                data.load().done();
                $("#popup").dxPopup("toggle", false);
                _this
                    .removeClass('text-primary')
                    .attr('data-value', '')
                    .attr('data-between', '')
                    .attr('data-expression', '');
            });
            clear.appendTo(div_footer);


            let div = $("<div/>").addClass('d-flex justify-content-end align-items-center');

            // button Ok
            let btnOk = $("<a/>").text('Ok').addClass('btn btn-outline-primary text-primary text-uppercase mr-2').css('border', '0').css('font-size', '0.9rem')
                .appendTo(div);

            // button Cancelar
            $("<a/>").text('Cancelar').addClass('btn btn-outline-primary text-primary text-uppercase').css('border', '0').css('font-size', '0.9rem').click(function () {
                $("#popup").dxPopup("toggle", false);
            })
                .appendTo(div);

            div.appendTo(div_footer);
            div_footer.appendTo(contentElement);

            if (dataType === 'string') {
            } else if (dataType === 'number') {

                $('.seletorInput').on('keyup', function () {
                    this.value = mascaraDeFormatacao3Digitos(this.value)
                });
                $('.seletorInputBetween').on('keyup', function () {
                    this.value = mascaraDeFormatacao3Digitos(this.value)
                });
            }

            //ONCLICK DO BOTAO OK
            btnOk.click(function () {
                //pegando o valor
                let value = contentElement[0].getElementsByClassName('seletorInput')[0].value;
                let valueBetween = contentElement[0].getElementsByClassName('seletorInputBetween')[0].value;

                //formatando o valor
                value = formatarValorFiltro(dataType, value, itemExampleValue);

                //verificando qual condicao está selecionada
                let domSelect = optionsFilterChange(contentElement, 'qual_selecionado', dataType);

                //aplicando a condicao do filtro
                if (domSelect === null || domSelect.toString() === "NaN") {
                } else {
                    if (domSelect !== "><") {
                        arrayOutrosFiltros.push([dataField, domSelect, value]);
                    } else {
                        if (valueBetween.indexOf(",") !== -1) {
                            valueBetween = valueBetween.replace(/[.]/g, "x").replace(/[,]/g, ".").replace(/[x]/g, "");
                        } else {
                            valueBetween = valueBetween.replace(/[.]/g, "");
                            valueBetween += '.00';
                        }
                        if (value < valueBetween) {
                            arrayOutrosFiltros.push([dataField, ">", value], [dataField, "<", valueBetween]);
                        } else {
                            arrayOutrosFiltros.push([
                                [dataField, "<", value],
                                [dataField, ">", valueBetween]
                            ]);
                        }
                        _this.attr('data-between', contentElement[0].getElementsByClassName('seletorInputBetween')[0].value);
                    }
                    data.filter(arrayOutrosFiltros);

                    _this.addClass('text-primary');
                    _this
                        .attr('data-value', contentElement[0].getElementsByClassName('seletorInput')[0].value)
                        .attr('data-expression', domSelect);
                    if (contentElement[0].getElementsByClassName('seletorInput')[0].value === "") {
                        _this.removeClass('text-primary');
                    }
                }
                //aplicando o filtro e fechando o modal
                data.load().done();
                $("#popup").dxPopup("toggle", false);
            });
        },
        //options
        showTitle: true,
        title: title,
        visible: true,
        dragEnabled: true,
        resizeEnabled: true,
        shading: false,
        closeOnOutsideClick: false,
        width: widthPopup,
        height: 240,
        minHeight: 240,
        maxHeight: 240,
    };
    if (popup) {
        popup.option("contentTemplate", popupOptions.contentTemplate.bind(this));
    } else {
        popup = $("#popup").dxPopup(popupOptions).dxPopup("instance");
    }
    popup.show();
    $('.dx-overlay-wrapper.dx-popup-wrapper').css('zIndex', '200');
};

// função para adição do filtro e o nome da coluna
function filterRow(container, options, headerDefault) {
    if (headerDefault === null || headerDefault === undefined) {
        headerDefault = true;
    }
    let dataField = options.column.dataField.toString();
    let dataSource = options.component._options._optionManager._options.dataSource;
    let dataType = options.column.dataType.toString();
    let title = options.column.caption.toString();
    let itemExampleValue;
    if (options.component._options._optionManager._options.dataSource._items.length > 0)
        itemExampleValue = options.component._options._optionManager._options.dataSource._items[0][dataField];
    else
        itemExampleValue = '0.00';
    let button = $("<span/>")
        .click(function (e) {
            dataField = options.column.dataField.toString();
            dataSource = options.component._options._optionManager._options.dataSource;
            dataType = options.column.dataType.toString();
            title = options.column.caption.toString();
            if (options.component._options._optionManager._options.dataSource._items.length > 0)
                itemExampleValue = options.component._options._optionManager._options.dataSource._items[0][dataField];
            else
                itemExampleValue = '0.00';

            e.preventDefault();
            showInfo(dataField, dataSource, dataType, button, title, itemExampleValue);
            $(".form-control.select2-single").select2({
                templateResult: formatStat, "language": {
                    "noResults": function () {
                        return ``;
                    }
                }, escapeMarkup: function (markup) {
                    return markup;
                }, theme: 'bootstrap'
            });
            e.stopPropagation();
        })
        .html(``)
        .attr('data-toggle', 'tooltip')
        .attr('data-placement', 'top')
        .attr('data-title', 'Filtro lógico')
        .attr('data-value', '')
        .attr('data-between', '')
        .attr('data-expression', '')
        .attr('data-field', dataField)
        .attr('data-type', dataType)
        .attr('data-item', itemExampleValue)
        .addClass('ml-2 seletorSpanFilter dx-icon-filter-condition mr-3');
    container.parent().find('.dx-column-indicators').append(button);
    if (headerDefault === true) {
        let text = $("<div/>")
            .html(options.column.caption);
        container.append(text);
    }
}