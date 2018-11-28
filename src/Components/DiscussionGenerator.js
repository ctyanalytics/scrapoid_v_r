/* 
 ----------------------------------------------------------
         DiscussionGenerator
 ----------------------------------------------------------
*/

import React from 'react';
import ListComponent from './ListComponents.js';
import MessageComponent_introduction from './MessageComponent_introduction';
import MessageComponent_discussion from './MessageComponent_discussion';
import MessageComponent_show from './MessageComponent_show';
import MessageComponent_input from './MessageComponent_input';
import Container from './Container.css';
import GetData from '../Data/GetData.js'


//url for back end
var url ='http://www.ctyanalytics.com/scrapoid_answer_react/';
         

//First Handshake 
const states = [ { i:0, state:"null",type_card:"null"} ]                
const transitions = [ {i:1, props : { type_card:"intro", text:"Hello I am scrapoid, I can scrap websites for you !", choices:["Let's get started"]}}  ]   
               

var _state_ = {
        items : {
                     },
       iteration: 0,
       current_state: "null"
       ,type_card:"null"
       //short term memory
       ,short_term_memory:{}
       };


class DiscussionGenerator extends React.Component
{
      
         constructor(props) {
                super(props);
            
                this.state = { items : {}};
                
                this.generate_card(_state_.iteration,_state_.current_state);
              }


       
      generate_card_back_end = async (iteration,current_state,type_card,short_term_memory) =>{
        try{
                        
                        // iteration , current state =>  next iteration, next props
                        var current_data= {url:url,iteration : iteration
                                , current_state:current_state ,short_term_memory:short_term_memory
                                };

                        var next_iteration=null;
                        var next_props=null;
                        
                        var response_data=await GetData(current_data);
                        console.log('---');
                        console.log(response_data);

                
                        next_iteration=response_data.i;
                        next_props=response_data.props;
                        type_card=next_props.type_card;
                        console.log('response is');
                        console.log(response_data);
                        if ("memorize" in response_data.props)
                        {
                                _state_.short_term_memory[response_data.props.memorize]=current_state
                              
                        } 

                        if ("memorize_data" in response_data.props)
                        {
                                _state_.short_term_memory["data"]=response_data.props.data
                              
                        }

                        console.log(_state_);
                        _state_.iteration=next_iteration;
                        _state_.type_card=type_card;
                        this.render_card(next_props); 
                }
                catch(error) {
                                console.error(error);
                                // expected output: SyntaxError: unterminated string literal
                                // Note - error messages will vary depending on browser
                              }
                
                }       

       generate_card =  (iteration,current_state) =>  {
               
        
        

                var next_iteration=null;
                var next_props=null;
                var type_card=null;
                var arrayLength = states.length;
                
                for (var j = 0; j < arrayLength;j++) {
                              
                                if ((states[j].i==iteration) && (states[j].state==current_state))
                                {    
                                        next_iteration=transitions[j].i;
                                        next_props=transitions[j].props;
                                        type_card=transitions[j].props.type_card;
                                        //update iteration as well
                                        _state_.iteration=next_iteration;
                                        _state_.type_card=type_card;
                                         this.render_card(next_props);    
                                }
                        }
                }

        render_card = (_props_) => {
               
                var timestamp = (new Date()).getTime();
                var last_ref="ref-"+timestamp;
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


                             
                                if  (_props_.type_card=='show') {  
                                   
                                        var item=  (
                                                <div>
                                                        <MessageComponent_show
                                                          text={_props_.text}
                                                          choices={_props_.choices}
                                                          onShow={this.onShow} 
                                                           ></MessageComponent_show> 
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

       onUpdate = async (val) => {
   
        _state_.current_state=val;
   
          await this.generate_card_back_end(_state_.iteration,_state_.current_state,_state_.type_card,_state_.short_term_memory) ;
       
       };

       onShow = async(val)=> {
  
           var selected_data=_state_.short_term_memory.data[val].data
           var $ = require('jquery');
           
          document.querySelector('#div_data_show').innerHTML=selected_data
          const $ = require('jquery');
          $.DataTable = require('datatables.net');
          var table = $('#table_result').DataTable({ "autoWidth": true});
          
          
       }
 

render  () { 
            return (
                    <div className="Container">
                       
                         < ListComponent   items={_state_.items} />
                    </div>
                    
                     
            );
         }
}

export default DiscussionGenerator;



