import './App.css';
import Buses from './components/Buses';
import Tickets from './components/Tickets';
import Trips from './components/Trips';
import Admin from './components/Admin';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
function App() {
  return (
    <Router>
      <Routes>
        {/* <Route index element={<Index />} /> */}
        {
          [
              {path: "/buses/", element: <Buses/>},
              {path: "/tickets/", element: <Tickets/>},
              {path: "/trips/", element: <Trips/>},
              {path: "/admin/", element: <Admin/>}
            
          ].map(route => <Route key={route.path} {...route}/>)
        }
      </Routes>
    </Router>
  )
}

export default App;
