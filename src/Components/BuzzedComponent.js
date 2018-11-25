

import React, { Component } from 'react'
import {Transition} from 'semantic-ui-react';



export default class BuzzedComponent extends Component {
    state = { visible: false }
  
    
    componentDidMount() {
      this.setState({ visible: !this.state.visible });
     }
  
     
    render() {
      const { visible } = this.state
      return (
        <div  >
  
          <Transition visible={visible} animation={this.props.animation}   duration={this.props.duration}  >
               { this.props.children }
          </Transition>
        </div>
      );
    }
  }
