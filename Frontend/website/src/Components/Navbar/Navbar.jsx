import '../Navbar/Navbar.css'


const Navbar = () => {
    return (
        <section className='navbar-container' id='navbar'>
            <h1 className='brand-name'>
                <span className='brand-name-black'>g</span>
                <span className='brand-name-black'>u</span>
                <span className='brand-name-green'>I</span>
                <span className='brand-name-green'>A</span>
                <span className='brand-name-black'>r</span>
            </h1>
            <div className='buttons'>
                <p className='brand-name-black brand-name-buttons' onClick={() => {document.getElementById('objective')?.scrollIntoView({ behavior: 'smooth' });}}>Objetivo</p>
                <p className='brand-name-black brand-name-buttons' onClick={() => {document.getElementById('team')?.scrollIntoView({ behavior: 'smooth' });}}>Equipa</p>
            </div>
        </section>
    )
}

export default Navbar;