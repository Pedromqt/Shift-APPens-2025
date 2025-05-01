import '../Pages/homepage.css'
import Navbar from "../Components/Navbar/Navbar";
import FirstSection from "../Components/FirstSection/FirstSection";
import Objective from '../Components/Objective/Objective';
import Team from '../Components/Team/Team';

const Homepage = () => {
    return(
        <div className='homepage'>
            <div className="first-section-homepage">
                {<Navbar/>}
                <div className='line'></div>
                {<FirstSection/>}
            </div>
            {<Objective/>}
            {<Team/>}
        </div>
        
    )
}

export default Homepage;