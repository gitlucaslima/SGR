let img = new Image();
let canvas = document.getElementById('UgCanvas');
let btnZoomMais = document.getElementById("btn-zoom-mais")
let btnZoomMenos = document.getElementById("btn-zoom-menos");
let formAssinatura = document.querySelector(".form-assinatura")
let imgInput = document.querySelector(".img-input");
let campo_imagem_base64 = document.querySelector("#campo_imagem_base64");
let btnCancelar = document.querySelector("#btn-cancelar");
canvas_width = canvas.width = 460;
canvas_height = canvas.height = 100;

let zoom = 1
let larguraImg;
let alturaImg;

let posicaoInicialX = 0;
let posicaoInicialY = 0;

let ctx = canvas.getContext('2d');
let imagem;
let movimentando = false

function draw(ctx, imagem, xi, yi, l, h) {
    ctx.clearRect(0, 0, canvas_width, canvas_height);
    ctx.drawImage(imagem, xi, yi, l, h);
}

function readImage() {
    if (this.files && this.files[0]) {
        var file = new FileReader();

        file.onload = function (e) {


            img.src = e.target.result;

            img.addEventListener('load', function () {
                larguraImg = img.width;
                alturaImg = img.height;
                
                draw(ctx, img, posicaoInicialX, posicaoInicialY, larguraImg, alturaImg)
                
            });

            
            btnZoomMenos.addEventListener("click", () => {
                
                zoom = 1 * (1 - 0.05);
                larguraImg = larguraImg * zoom;
                alturaImg = alturaImg * zoom;

               
                draw(ctx, img, posicaoInicialX, posicaoInicialY, larguraImg, alturaImg)


            })

            btnZoomMais.addEventListener("click", () => {

                zoom = 1 * (1 + 0.05);
                larguraImg = larguraImg * zoom;
                alturaImg = alturaImg * zoom;

              
                draw(ctx, img, posicaoInicialX, posicaoInicialY, larguraImg, alturaImg)


            })

            canvas.style.cursor = "all-scroll"

            canvas.addEventListener("mousedown", () => {
                movimentando = true

                canvas.style.cursor = "all-scroll"

            })

            canvas.addEventListener("mouseup", () => {
                movimentando = false

                canvas.style.cursor = "all-scroll"

            })

            canvas.addEventListener("mousemove", (event) => {


                if (movimentando) {

                    let x;
                    let y;
                    x = event.movementX;
                    y = event.movementY;

                    posicaoInicialX = posicaoInicialX + x;
                    posicaoInicialY = posicaoInicialY + y;

                
                    draw(ctx, img, posicaoInicialX, posicaoInicialY, larguraImg, alturaImg)

                }
            })


            formAssinatura.addEventListener("submit",(event)=>{

                let imagem_base64 = canvas.toDataURL();
                imagem_base64 = imagem_base64.replace("data:image/png;base64,",'')
                
                campo_imagem_base64.value = imagem_base64;
               
            }) 


        };
        
        file.readAsDataURL(this.files[0]);
    }


}

document.querySelector(".img-input").addEventListener("change", readImage, false)
btnCancelar.addEventListener("click",()=>{

    ctx.clearRect(0, 0, canvas_width, canvas_height);
    mostrarMensagem();
})

function mostrarMensagem(){

    ctx.font = '20px arial';
    ctx.fillText("Sua assinatura aparecerar aqui",90,40)

}

mostrarMensagem()