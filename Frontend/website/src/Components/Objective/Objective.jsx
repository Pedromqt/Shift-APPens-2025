import "../Objective/Objective.css"

const Objective = () => {
    return(
        <section className="objective-container" id="objective">
            <h1 className="objective-title">
                Objetivo
            </h1>
            <div className="objective-text">
                O objetivo deste projeto é desenvolver um software que, utilizando uma câmara, microfone e audio juntamente com inteligência artificial, GPS e assistente de voz, seja capaz de detetar objetos, pessoas, obstáculos e perigos no caminho, como buracos, degraus e qualquer tipo de veículo. Esta tecnologia é pensada especialmente para pessoas cegas ou com visão mais reduzida, oferecendo-lhes maior autonomia, segurança e confiança na deslocação diária. Combinando deteção em tempo real, orientação por áudio e comandos por voz, pretendemos criar uma solução acessível e inclusiva que transforme a mobilidade assistida.
            </div>
        </section>
    )
}

export default Objective;