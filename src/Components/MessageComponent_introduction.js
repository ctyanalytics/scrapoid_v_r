import React, { Component } from 'react'
import Scroll from 'react-scroll';
import GetData from '../Data/GetData.js'

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
    console.log(GetData());
    
   
   
  };
    render() {
      if ((this.props.elem_loading) !==undefined) { this.props.elem_loading.style.display="none";}
      return (
        <div className="Container_messages">
              <div className="ui centered card" >
          
                          <div className="image">
                        
                            <img src="./scrapoid.png" />
                        
                          </div>
                          
                          <div className="content">
                        
                              <a className="header" >{this.props.text}</a>
                            
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
              </div>
        
      );
    }
  }


  
  