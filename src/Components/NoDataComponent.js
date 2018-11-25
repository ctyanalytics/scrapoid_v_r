

import React, { Component } from 'react'
import Container_data from './Container_data.css';


export default class NoDataComponent extends Component {

    render() {
     
      return (
     
       
        <div  className="Container_data">
            <list>
                            <h2 class="ui grey inverted header">No data to display</h2>
                            <div class="ui inverted segment">
                            <div class="ui active inverted placeholder">
                            <div class="image header">
                            <div class="line"></div>
                            <div class="line"></div>
                            </div>
                            <div class="paragraph">
                            <div class="line"></div>
                            <div class="line"></div>
                            <div class="line"></div>
                            </div>
                            </div>
                            </div>
                
                    </list>
        </div>
      );
    }
  }