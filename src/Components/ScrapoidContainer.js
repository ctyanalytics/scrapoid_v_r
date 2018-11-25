import React from 'react';
import DiscussionGenerator from './DiscussionGenerator.js';
import NoDataComponent from './NoDataComponent.js';


const ScrapoidContainer = () => {

return (
        <div style={{backgroundColor:"black" }} class="ui stackable two column   grid">
                        <div class="column">
                                <DiscussionGenerator />       
                        </div>
                        <div class="column">
                                  <NoDataComponent  /> 
                        </div>
                        
       </div>
       
)
   
}

export default ScrapoidContainer;