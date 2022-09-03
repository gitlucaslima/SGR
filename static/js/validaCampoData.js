

const selectMesRelatorio = document.querySelector(".select-mes-relatorio");
const inputDateLimite = document.querySelector(".input-date-limite");

const selectMesRelatorioEdit = document.querySelectorAll(".select-edit");
const inputDateLimiteEdit = document.querySelectorAll(".input-edit");
const anoCadastro = document.querySelector("#ano-cadastro");

function redefinirMinDate(itemInputDate, selectMes) {

    itemInputDate.disabled = false
    let ano = itemInputDate.min.split("-")[0]
    let mes = selectMes.value.length == 2 ? selectMes.value : "0" + selectMes.value
    let dia = itemInputDate.min.split("-")[2]

    data = `${ano}-${mes}-${dia}`
    console.log(data)
    itemInputDate.min = data

}


selectMesRelatorio.addEventListener("click", () => {



    redefinirMinDate(inputDateLimite, selectMesRelatorio)

    inputDateLimite.value = inputDateLimite.min;


})

selectMesRelatorioEdit.forEach(itemSelecte=>{

    itemSelecte.addEventListener("click", () => {

        inputDateLimiteEdit.forEach(itemInput=>{

            redefinirMinDate(itemInput, itemSelecte)
    
            itemInput.value = itemInput.min;
            
            let [ano, mes, dia] = itemInput.value.split("-");
            mes = itemSelecte.value.length == 2 ? itemSelecte.value : '0' + itemSelecte.value;
        
            itemInput.value = `${ano}-${mes}-${dia}`;
    
        })

    })

})

