/* 
 ----------------------------------------------------------
         DiscussionGenerator
 ----------------------------------------------------------
*/

import React from 'react';
import ListComponent from './ListComponents.js';
import MessageComponent_introduction from './MessageComponent_introduction';
import MessageComponent_discussion from './MessageComponent_discussion';
import MessageComponent_input from './MessageComponent_input';
import Container from './Container.css';




                                
const states = [ { i:0, state:"null"} , 
                 {i:1, state:"Let's get started"} ,
                 {i:2, state:"This"},
                 {i:2, state:"That"}
                ]   
const transitions = [ {i:1, props : { type_card:"intro", text:"Hello I am scrapoid, I can scrap websites for you !", choices:["Let's get started"]}} ,
                      {i:2, props : { type_card:"discussion", text:"What do you want ? ", choices:["This","That"]}  } ,
                      {i:3, props : { type_card:"input", text:"Ok please give me This"}  },
                      {i:3, props : { type_card:"input", text:"Ok please give me that"}  }
                
                ]

var _state_=         _state_ = {
        items : {
                     },
       iteration: 0,
       current_state: "null"
       };

var last_ref="";

class DiscussionGenerator extends React.Component
{
      
        constructor(props) {
                super(props);
            
                this.state = { items : {}};
        

                this.generate_card(_state_.iteration,_state_.current_state);
              }
       
       generate_card = (iteration,current_state) =>  {
               
        
                var next_iteration=null;
                var next_props=null;
                var arrayLength = states.length;
                
                for (var j = 0; j < arrayLength;j++) {
                              
                                if ((states[j].i==iteration) && (states[j].state==current_state))
                                {    
                                        next_iteration=transitions[j].i;
                                        next_props=transitions[j].props;
                                      
                                        //update state as well
                                        _state_.iteration=next_iteration;
                              
                                this.render_card(next_props);
                                   
                                               
                                     
                                }
                
                        }



                }

        render_card = (_props_) => {
                var timestamp = (new Date()).getTime();
                last_ref="ref-"+timestamp;
                        if  (_props_.type_card=='intro') {  

                                        var item=  (
                                        <div>
                                                <MessageComponent_introduction 
                                                text={_props_.text}
                                                onUpdate={this.onUpdate}
                                                choices={_props_.choices}
                                            
                                                >
                                                
                                                </MessageComponent_introduction> 
                                              
                                        </div>
                                        );
                                }
                             
                                if  (_props_.type_card=='discussion') {  
                                   
                                        var item=  (
                                                <div>
                                                        <MessageComponent_discussion 
                                                         onUpdate={this.onUpdate} 
                                                          text={_props_.text}
                                                          choices={_props_.choices}
                                                        
                                                           ></MessageComponent_discussion> 
                                                </div>
                                                );
                                }

                                if  (_props_.type_card=='input') {  
                                   
                                        var item=  (
                                                <div>
                                                        <MessageComponent_input 
                                                         onUpdate={this.onUpdate} 
                                                          text={_props_.text}
                                                         
                                                        
                                                           ></MessageComponent_input> 
                                                </div>
                                                );
                                }
           
                        this.addItem(item);
                              
                                };


       addItem = (item) =>  {
        //create a unike key for each new  item
        var timestamp = (new Date()).getTime();
        // update the state object
        _state_.items['item-' + timestamp ] = item;
   
     
     
       this.setState({ items : _state_.items })
      
       };

       onUpdate = (val) => {
        

        _state_.current_state=val;
   
          this.generate_card(_state_.iteration,_state_.current_state);
       
         
        
      
      
       
       };
 

render() {
            return (
                    <div className="Container">
                         < ListComponent   items={_state_.items} />
                    </div>
            );
         }
}

export default DiscussionGenerator;



