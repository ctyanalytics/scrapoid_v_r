import React from 'react';
import DiscussionGenerator from './DiscussionGenerator.js';
import NoDataComponent from './NoDataComponent.js';
import  ScrollArea from 'react-scrollbar'
import { Grid, GridColumn } from 'semantic-ui-react'

const ScrapoidContainer = () => {

return (
        <Grid style={{backgroundColor:"black" }} stackable >
                        <GridColumn  width={5}   >
                        <ScrollArea style={{ height: 600 }}
                        
                        speed={0.8}
                        className="area"
                        contentClassName="content"
                        horizontal={false}
                        >
                                <DiscussionGenerator />  
                                </ScrollArea>     
                        </GridColumn>
                        <GridColumn   width={11}  id="div_data_show">
                                  <NoDataComponent  /> 
                        </GridColumn>
                        
       </Grid>
       
)
   
}

export default ScrapoidContainer;