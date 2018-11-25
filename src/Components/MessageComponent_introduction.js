import React, { Component , Icon} from 'react'
import {Message} from 'semantic-ui-react';
import BuzzedComponent from './BuzzedComponent.js';
import Scroll from 'react-scroll';

export default class MessageComponent_introduction extends Component {
  
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
      if ((this.props.elem_loading) !==undefined) { this.props.elem_loading.style.display="none";}
      return (
              <div className="ui centered card" >
          
                          <div className="image">
                        
                            <img src="./scrapoid.png" />
                        
                          </div>
                          
                          <div className="content">
                        
                              <a className="header">{this.props.text}</a>
                            
                          </div>

                           <div className="extra content">
                                        <div className="small ui buttons">
                                        
                                            {this.props.choices.map(
                                              (choice, index)=>{
                                              return (
                                              <div>
                                              <div className="ui  black button"  key={ index }  onClick={this.update}>{choice}</div>
                                              </div>
                                              )
                                            })}
                                            </div>
                                        </div>
                    
                      
              </div>
        
      );
    }
  }


  
  