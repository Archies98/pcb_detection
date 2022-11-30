import React, { Component } from "react";
import "./App.css";
import Upload from "./upload/Upload";
import Menu, {items} from "./menu/script";


class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="menu">
          <Menu items={items}/>
        </div>
        <div className="Card">
          <Upload />
        </div>
      </div>
    );
  }
}

export default App;
