import React, { Component }  from 'react'
import DashBoardScrapoidComponent from './DashBoardScrapoidComponent.js';
import {
  Container,
  Divider,
  Dropdown,
  Grid,
  Header,
  Image,
  List,
  Menu,
  Segment,
  Icon
} from 'semantic-ui-react'
var Content =<div></div>;
export default class FixedMenuLayout extends Component {
    constructor(props) {
        super(props);
       
    this.state = { 
        content: <div></div> }

            }
render()
{
    return (
  <div>
    <Menu fixed='top' inverted>
      <Container>
        <Menu.Item as='a' header onClick={()=> this.setState({content:<div></div>})}>
          <Icon name='pie graph'></Icon>
          Dashboard
        </Menu.Item>
        <Menu.Item as='a' onClick={()=> this.setState({content:<div></div>})}>
        <Icon name='home'></Icon>
        Home</Menu.Item>

        <Menu.Item as='a' onClick={()=> this.setState({content:<DashBoardScrapoidComponent></DashBoardScrapoidComponent>})}>
        <Icon name='smile'></Icon>
        Scrapoid</Menu.Item>
        
      </Container>
    </Menu>

    <Container style={{ marginTop: '7em' }}>
       {this.state.content}
    </Container>

    
    
  </div>
    );
}
}

