
const tabConfiguracao = document.querySelectorAll(".tab-configuracao");



tabConfiguracao.forEach(item=>{

    item.addEventListener('click',()=>{

        let valor = item.getAttribute("data-opcao-tab");
        
        let urls = window.location.href.split("/")

        let urlModificada = urls[0] + '//' + urls[2] + "/" + urls[3] + '/' + valor;

        window.location.href = urlModificada
    })

})
