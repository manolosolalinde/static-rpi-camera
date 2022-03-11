// import './App.css';
import './css/general.css';
import './css/range-slider.css';
import './css/switch.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Settings from './components/settings';
import StreamImage from './components/stream_image';
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
          <StreamImage />
          <Settings />
        </main>
      </div>
    </SocketContext.Provider>
  );
}

export default App;
