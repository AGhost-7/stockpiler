import React, { Component } from 'react';
import logo from '../img/logo.svg';
import '../css/App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Stockpiler</h1>
        </header>
        <p className="App-intro">
					Stock management and organized sales tracking.
				</p>
      </div>
    );
  }
}

export default App;
