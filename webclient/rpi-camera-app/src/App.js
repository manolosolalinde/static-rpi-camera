// import './App.css';
import './css/general.css';
import './css/range-slider.css';
import './css/switch.css';
import './css/controller.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Settings from './components/settings';
import React from 'react';
import {SocketContext, socket } from './context/socket';



function App() {
  return (
    <SocketContext.Provider value={socket}>

      <div className="App">
        {/* <header className="App-header">
        <h1>header settings</h1>
      </header> */}
        <main>
          <Settings />
        </main>
      </div>
    </SocketContext.Provider>
  );
}

export default App;
