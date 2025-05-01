import '../FirstSection/FirstSection.css'


const FirstSection = () => {
    return (
    <div className='first-section-container'>
        <h1 className='brand-name-first-section'>
            <span className='welcome-text'>Welcome to </span>
            <span className='brand-name-black'>g</span>
            <span className='brand-name-black'>u</span>
            <span className='brand-name-green'>I</span>
            <span className='brand-name-green'>A</span>
            <span className='brand-name-black'>r</span>
        </h1>
        <div className='middle-part-text'>
            <span className='brand-name-green'>I</span>
            <span className='brand-name-green'>A </span>
            para guiar quem mais precisa
        </div>
    </div>
    )
}

export default FirstSection;