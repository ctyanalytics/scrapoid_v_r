import React, { Component } from 'react'
import BuzzedComponent from './BuzzedComponent.js';
import Delayed from './Delayed.js';
import Scroll from 'react-scroll';
var current_input=""
export default class MessageComponent_discussion extends Component {
    constructor(props) {
        super(props);
       
        this.state = {
          fieldVal: "init"
        }
      }

      componentDidMount() {
        var scroll     = Scroll.animateScroll;
        scroll.scrollToBottom();
    }

      
      update = (event) => {
  
        this.setState({fieldVal: current_input});
        this.props.onUpdate(current_input);
       
 
        
     
      };

      update_value = (event) => {
  
        current_input=event.currentTarget.value;
    
      };

     

     
   
    render() {
     
     
       return(
         
        <Delayed waitBeforeShow={1000}>
 <div className="Container_messages">
        <div className="ui card" >
            <div className="content">
                    <div className="center aligned header">{this.props.text}</div>
                    <div className="center aligned description">
                    < BuzzedComponent animation="jiggle"  duration={1000}>
                                     <div className="extra content">
                                       <div className="ui action input" >
                                            <input type="text" placeholder="your url here ..." onChange={this.update_value}/>
                                            <div  className="ui  black button"   onClick={this.update} >Send</div>
                                            </div>
                                        </div>
                                        </BuzzedComponent>
                    </div>
            </div>
            <div className="extra content">
                    <div className="center aligned author">
                        <img className="ui avatar image" src="./scrapoid.png"></img>
                        </div>
            </div>
     
      </div>
      </div>
      </Delayed>
    
       )
    }
  }



