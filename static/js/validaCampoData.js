

const selectMesRelatorio = document.querySelectorAll(".select-mes-relatorio");
const inputDateLimite = document.querySelectorAll(".input-date-limite");

const selectMesRelatorioEdit = document.querySelectorAll(".select-edit");
const inputDateLimiteEdit = document.querySelectorAll(".input-edit");

function redefinirMinDate(itemInputDate,selectMes){

    let ano = itemInputDate.min.split("-")[0]
    let mes = selectMes.value.length == 2 ? selectMes.value : "0" + selectMes.value
    let dia = itemInputDate.min.split("-")[2]
    
    data = `${ano}-${mes}-${dia}`
    itemInputDate.min = data
}

selectMesRelatorio.forEach(item => {

    item.addEventListener("click", () => {
       
        inputDateLimite.forEach(itemInput => {
          
            itemInput.disabled = false;
           
            redefinirMinDate(itemInput,item)

    })   

})})


selectMesRelatorioEdit.forEach(item => {

    item.addEventListener("click", () => {
       
        inputDateLimiteEdit.forEach(itemInput => {
            
          
            itemInput.disabled = false;

            redefinirMinDate(itemInput,item)    

    })
})})