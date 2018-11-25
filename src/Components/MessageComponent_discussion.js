import React, { Component } from 'react'
import {Message} from 'semantic-ui-react';
import BuzzedComponent from './BuzzedComponent.js';
import Delayed from './Delayed.js';
import Scroll from 'react-scroll';
import Container_messages from './Container_messages.css';

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
   
        this.setState({fieldVal:event.currentTarget.textContent});
        this.props.onUpdate(event.currentTarget.textContent);
      
 
        
     
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
                                     <div >
                                   
                                       
                                            {this.props.choices.map((choice, index)=>{
                                              return (
                                               
                                              <div className="ui  black button"  key={ index }
                                                onClick={this.update}>{choice}</div>
                                           
                                              )
                                            })}
                                          
                                           
                                          
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



