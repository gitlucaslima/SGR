

const selectMesRelatorio = document.querySelector(".select-mes-relatorio");
const inputDateLimite = document.querySelector(".input-date-limite");

const selectMesRelatorioEdit = document.querySelector(".select-edit");
const inputDateLimiteEdit = document.querySelector(".input-edit");


function redefinirMinDate(itemInputDate, selectMes) {

    let ano = itemInputDate.min.split("-")[0]
    let mes = selectMes.value.length == 2 ? selectMes.value : "0" + selectMes.value
    let dia = itemInputDate.min.split("-")[2]

    data = `${ano}-${mes}-${dia}`
    itemInputDate.min = data

}


selectMesRelatorio.addEventListener("click", () => {

    inputDateLimite.disabled = false;

    redefinirMinDate(inputDateLimite, selectMesRelatorio)

    inputDateLimite.value = inputDateLimite.min;


})

selectMesRelatorioEdit.addEventListener("click", () => {


    inputDateLimiteEdit.disabled = false;

    redefinirMinDate(inputDateLimiteEdit, selectMesRelatorioEdit)

    inputDateLimiteEdit.value = inputDateLimiteEdit.min;
    
    let [ano, mes, dia] = inputDateLimiteEdit.value.split("-");
    mes = selectMesRelatorioEdit.value.length == 2 ? selectMesRelatorioEdit.value : '0' + selectMesRelatorioEdit.value;

    inputDateLimiteEdit.value = `${ano}-${mes}-${dia}`;

})

function reajustarSelect(input, select) {

    let [ano, mes, dia] = input.value.split("-")

    console.log(parseInt(mes))
    console.log(parseInt(select.value))
    if(parseInt(mes) < parseInt(select.value)){

    
        select.value = parseInt(mes)
    }

}

inputDateLimite.addEventListener("input", () => {


    reajustarSelect(inputDateLimite,selectMesRelatorio)

})

inputDateLimiteEdit.addEventListener("input", () => {


    reajustarSelect(inputDateLimiteEdit,selectMesRelatorioEdit)

})

